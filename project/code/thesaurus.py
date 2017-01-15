"""
Author: Joris van Vugt

Create thesauris from wordvectors
"""
import sys
import pickle
import xml.etree.ElementTree as ET

from tqdm import tqdm
import numpy as np
from scipy.spatial.distance import pdist, squareform

def build_from_xml(input_file):
    """
    Build a thesauris dictionary using
    https://data.overheid.nl/OpenDataSets/justitiethesaurus_2015.xml
    """
    root = ET.parse(input_file)

    thesaurus = {}
    for descriptor in tqdm(root.findall('descriptor')):
        word = descriptor.find('descriptor-term').text.lower()
        # Group all types of related words
        related = [e.text for e in descriptor.findall('related-term')]
        narrow = [e.text for e in descriptor.findall('narrow-term')]
        broader = [e.text for e in descriptor.findall('broader-term')]
        use = [e.text for e in descriptor.findall('use')]
        used_for = [e.text for e in descriptor.findall('used-for')]
        relevant = related + narrow + broader + use + used_for
        relevant = [w.lower().replace(' ', '_') for w in relevant]

        thesaurus[word] = relevant

    with open(input_file + '.ths', 'wb') as file:
        pickle.dump(thesaurus, file)


def build_from_w2v(input_file, n=20):
    """
    Build a thesauris from a Word2Vec model
    The n most similar words are chosen as related

    The current implementation is quite slow and memory intensive
    """
    print('Loading model...')
    with open(input_file, 'rb') as file:
        model = pickle.load(file)

    with open('D:/Data/justitiethesaurus_2015.xml.ths', 'rb') as file:
        ground_truth = pickle.load(file)

    relevant_words = set(sum([[word] + ground_truth[word] for word in ground_truth.keys()], []))

    print('Calculating distances...')
    words = sorted(word.replace(' ', '_') for word in model.keys() if word in relevant_words)
    print('%d words in vocabulary' % len(words))
    vectors = np.zeros((len(words), len(model[words[0]])), dtype=np.float32)
    for i, word in enumerate(tqdm(words)):
        vectors[i, :] = model[word]
    dists = squareform(pdist(vectors, 'cosine'))
    print('Computing top_n words....')
    top_n = np.argsort(dists, axis=1)[:, 1:n]
    print('Building thesaurus...')
    thesaurus = {}
    for i, word in enumerate(tqdm(words)):
        thesaurus[word] = [words[top] for top in top_n[i]]

    with open(input_file + '.ths', 'wb') as file:
        pickle.dump(thesaurus, file)



def build_thesauris(input_file):
    """
    Build a thesauris from an xml file or a W2V model
    """
    if input_file[-4:] == '.xml':
        build_from_xml(input_file)
    else:
        build_from_w2v(input_file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:\n python {} model'.format(__file__))
    else:
        build_thesauris(sys.argv[1])

