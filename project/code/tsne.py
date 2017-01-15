import sys
import pickle

import numpy as np
from sklearn.manifold import TSNE


def run(filename):
    with open(filename, 'rb') as file:
        model = pickle.load(filename)
    words = sorted(model.keys())
    vectors = np.zeros((len(words), len(model[words[0]])), dtype=np.float32)
    for i, word in enumerate(words):
        vectors[i, :] = model[word]
    tsne = TSNE()
    embeddings = tsne.fit_transform(vectors)
    with open(filename + '.out', 'wb') as file:
        pickle.dump(embeddings, file)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:\n python {} vectors'.format(__file__))
    else:
        run(sys.argv[1])
