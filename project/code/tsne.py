import sys
import pickle

import numpy as np
from sklearn.manifold import TSNE


def run(filename, ground_truth):
    with open(filename, 'rb') as file:
        model = pickle.load(file)

    with open('D:/Data/justitiethesaurus_2015.xml.ths', 'rb') as file:
        ground_truth = pickle.load(file)

    relevant_words = set(sum([[word] + ground_truth[word] for word in ground_truth.keys()], []))
    words = sorted(word.replace(' ', '_') for word in model.keys() if word in relevant_words)
    vectors = np.zeros((len(words), len(model[words[0]])), dtype=np.float32)
    for i, word in enumerate(words):
        vectors[i, :] = model[word]
    tsne = TSNE()
    embeddings = tsne.fit_transform(vectors)
    with open(filename + '.out', 'wb') as file:
        pickle.dump(embeddings, file)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage:\n python {} vectors ground_truth'.format(__file__))
    else:
        run(sys.argv[1], sys.argv[2])
