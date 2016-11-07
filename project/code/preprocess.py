"""
Author: Joris van Vugt

Preprocess an XML file from rechtspraak.nl
"""
import glob
import re
import pickle
from unidecode import unidecode

from tqdm import tqdm

DATA_FOLDER = 'D:\\Data\\rechstpraak.nl'

def clean(word):
    """
    Convert a word to lowercase and remove all
    non-alphanumeric characters
    """
    return re.sub('[^\w-]', '', word.lower())

def preprocess():
    """
    Preprocess all XML-files in the specified folder

    Remove the XML-tags and clean the remaining raw text
    """
    files = glob.glob(DATA_FOLDER + '/raw/*.xml')
    tag_regex = re.compile('<[^>]*>')
    buffer = []
    for file_name in tqdm(files):
        with open(file_name, 'r', encoding='utf-8') as file:
            try: 
                text = unidecode(file.read())
                # Remove all XML tags
                text = tag_regex.sub('', text)
                lines = text.splitlines()
                # Remove abundant whitespace
                lines = [line.strip() for line in lines]
                words = [[clean(word) for word in line.split()] 
                                for line in lines if line != '']
                buffer += words
            except UnicodeError:
                print('Skipping {}, UnicodeError'.format(file_name))

    # Save the preprocessed data           
    with open(DATA_FOLDER + '/processed/output.pkl', 'wb') as out_file:
        pickle.dump(buffer, out_file)




if __name__ == '__main__':
    preprocess()