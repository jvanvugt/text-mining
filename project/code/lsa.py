"""
Author: Joris van Vugt

Use techniques from latent semantic analysis to build a thesaurus
"""
import glob
import sys
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
from tqdm import trange

def cosine_similarity(a, b):
    """Compute the cosine similarity between 2 vectors"""
    return a.T.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b))

def read_file(filename):
    """Open a file and return its content"""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def build_thesaurus(model, words, top_n=5):
    """
    Build a thesaurus based on the topic distributions from the model
    """
    thesaurus = {}
    dist = model.components_
    n_words = len(words)
    for word_idx in trange(n_words):
        sims = [cosine_similarity(dist[:, word_idx], dist[:, other])
                for other in range(n_words)]
        top_n_words = np.argsort(sims)[:-top_n-2:-1][:1]
        related_words = [words[i] for i in top_n_words]
        thesaurus[words[word_idx]] = related_words
    return thesaurus

def build_model(input_folder, output_file):
    """
    Train LDA on  the term-document matrix from all .txt
    documents in input_folder.
    """
    print('Loading data...')
    files = glob.glob(input_folder + '/*.txt')
    data = [read_file(file_name) for file_name in files]
    print('Creating tf-matrix...')
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=50, stop_words=None)
    tf = tf_vectorizer.fit_transform(data)
    print('Training model...')
    lda = LatentDirichletAllocation(n_topics=100, max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0,
                                    n_jobs=3)
    lda.fit(tf)
    print('Building thesaurus...')
    words = tf_vectorizer.get_feature_names()
    thesaurus = build_thesaurus(lda, words)
    with open(output_file, 'wb') as out_file:
        pickle.dump(thesaurus, out_file)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage:\npython {} input_folder output_file'.format(__file__))
    else:
        build_model(sys.argv[1], sys.argv[2])
