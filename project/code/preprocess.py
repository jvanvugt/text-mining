"""
Author: Joris van Vugt

Preprocess an XML file from rechtspraak.nl
"""
import glob
import re
import pickle
import sys
import os
import ntpath

from unidecode import unidecode
from tqdm import tqdm
    

def preprocess(input_folder, output_folder):
    """
    Preprocess all XML-files in the specified folder
    The cleaned files will be saved in the output folder

    Remove the XML-tags and clean the remaining raw text
    to have one sentence per line
    """
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    files = glob.glob(input_folder + '/*.xml')
    tag_regex = re.compile('<[^>]*>')
    eos_regex = re.compile(r'(\w)\. ([A-Z])')
    for file_name in tqdm(files):
        with open(file_name, 'r', encoding='utf-8') as file:
            try: 
                text = unidecode(file.read())
                # Remove all XML tags
                text = tag_regex.sub('', text)
                lines = text.splitlines()
                # Remove abundant whitespace
                lines = [line.strip() for line in lines]
                # One sentence per line
                lines = [eos_regex.sub('\\1.\n\\2', line) for line in lines]
                # Remove empty lines
                lines = [line for line in lines if line != '']
                # Change extension to .txt
                outfile = ntpath.basename(file_name)[:-4] + '.txt'
                out_name = os.path.join(output_folder, outfile)
                with open(out_name, 'w', encoding='utf-8') as out:
                    out.write('\n'.join(lines))
            except UnicodeError:
                print('Skipping {}, UnicodeError'.format(file_name))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {} input_folder output_folder'.format(__file__))
    else:
        print(sys.argv)
        preprocess(sys.argv[1], sys.argv[2])