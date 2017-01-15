"""
Author: Joris van Vugt

Use techniques from latent semantic analysis to build a thesaurus
"""
import glob
import sys
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.externals import joblib
import pickle


def read_file(filename):
    """Open a file and return its content"""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def build_vectors(model, words):
    """
    Build a a dictionary of vectors based on the topic distributions from the model
    """
    dist = model.components_
    n_words = len(words)
    vectors = {}
    for word_idx in range(n_words):
        vectors[words[word_idx]] = dist[:, word_idx]
    return vectors

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
    vectors = build_vectors(lda, words)
    with open(output_file, 'wb') as out_file:
        pickle.dump(vectors, out_file)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage:\npython {} input_folder output_file'.format(__file__))
    else:
        vectors = build_vectors(joblib.load(sys.argv[1]), joblib.load(sys.argv[2]).get_feature_names())
        pickle.dump(vectors, open(sys.argv[1] + 'vectors', 'wb'))
        # build_model(sys.argv[1], sys.argv[2])
