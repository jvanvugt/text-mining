"""
Author: Joris van Vugt

Create thesauris from wordvectors
"""
import sys
import pickle
import xml.etree.ElementTree as ET

from gensim.models import Word2Vec
from tqdm import tqdm

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


def build_from_w2v(input_file, n=5):
    """
    Build a thesauris from a Word2Vec model
    The n most similar words are chosen as related

    The current implementation is quite slow and memory intensive
    """
    print('Loading model...')
    model = Word2Vec.load_word2vec_format(input_file, binary=True)
    print('Building thesauris...')
    thesaurus = {}
    for word in tqdm(model.vocab):
        thesaurus[word] = [w[0] for w in model.most_similar([word], topn=n)]

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

