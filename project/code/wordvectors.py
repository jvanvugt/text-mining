"""
Author: Joris van Vugt

Train a Word2Vec model
"""

import sys
import glob

from gensim.models import Word2Vec

def read_file(filepath):
    """
    Read a file and convert it to a list of sentences
    The sentences are lists of words
    """
    with open(filepath) as file:
        lines = file.read().splitlines()
        return [line.split() for line in  lines]

def concatenate_files(input_folder):
    """
    Concatenate the contents of all .txt
    files in input_folder into a single list
    """
    files = glob.glob(input_folder + '/*.txt')
    contents = [read_file(f) for f in files]
    return sum(contents, [])

def train_model(input_folder, output_file):
    """
    Train a Word2Vec model on the .txt files in
    input_folder. The resulting model will be
    saved in output_file
    """
    sentences = concatenate_files(input_folder)
    model = Word2Vec(sentences, workers=3)
    model.save(output_file)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {} input_folder output_file'.format(__file__))
    else:
        train_model(sys.argv[1], sys.argv[2])