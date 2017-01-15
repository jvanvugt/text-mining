"""
Author: Joris van Vugt

Use techniques from latent semantic analysis to build a thesaurus
"""
import glob
import sys
import pickle

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.externals import joblib
from sklearn.pipeline import make_pipeline


def read_file(filename):
    """Open a file and return its content"""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def build_vectors(model, words):
    """
    Build a a dictionary of vectors based on the topic distributions from the model
    """
    dist = model
    n_words = len(words)
    vectors = {}
    for word_idx in range(n_words):
        vectors[words[word_idx]] = dist[word_idx, :]
    return vectors

def build_model(input_folder, output_file):
    """
    Perform LSA on  the term-document matrix from all .txt
    documents in input_folder.
    """
    print('Loading data...')
    files = glob.glob(input_folder + '/*.txt')
    data = [read_file(file_name) for file_name in files]
    print('Creating tf-matrix...')
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=20, sublinear_tf=True)
    tfidf = tfidf_vectorizer.fit_transform(data)
    print('Training model...')
    svd = TruncatedSVD(n_components=100)
    lsa = make_pipeline(svd, Normalizer(copy=False))
    lsa.fit(tfidf)
    words = tfidf_vectorizer.get_feature_names()
    model = lsa.transform(np.eye(len(words)))
    print('Building thesaurus...')
    vectors = build_vectors(model, words)
    
    for _ in range(10):
        word = np.random.choice(words)
        dists = [np.linalg.norm(vectors[word] - vectors[other]) for other in words]
        print('%s: %s\n' % (word, ', '.join([words[i] for i in np.argsort(dists)[:10]])))

    with open(output_file, 'wb') as out_file:
        pickle.dump(vectors, out_file)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage:\npython {} input_folder output_file'.format(__file__))
    else:
        build_model(sys.argv[1], sys.argv[2])
