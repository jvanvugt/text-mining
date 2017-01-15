import sys
import pickle

import matplotlib.pyplot as plt
plt.style.use('ggplot')

def run(filename):
    with open(filename, 'rb') as emb_f, \
         open('D:/Data/rechtspraak.nl/vectors.pkl.ths', 'rb') as v_f, \
         open('D:/Data/justitiethesaurus_2015.xml.ths', 'rb') as v_t:
        embeddings = pickle.load(emb_f)
        model = pickle.load(v_f)
        ground_truth = pickle.load(v_t)

    relevant_words = set(sum([[word] + ground_truth[word] for word in ground_truth.keys()], []))
    words = sorted(word.replace(' ', '_') for word in model.keys() if word in relevant_words)
    plt.scatter(embeddings[:, 0], embeddings[:, 1])
    for i in range(len(words)):
        plt.annotate(s=words[i], xy=(embeddings[i, 0], embeddings[i, 1]), xytext=(-20, 10), textcoords='offset points')
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python {} embeddings'.format(__file__))
    else:
        run(sys.argv[1])