"""
Author: Joris van Vugt

Assignment for week 2 of Text Mining
"""
import sys
import re

def clean(filename):
    """
    Reformat the given file to have one sentence per line
    The result is written to filename.out
    """
    with open(filename) as file:
        text = ''.join(file.readlines())
        
        # The file contains 'soft-hyphens', these are replaced with
        # normal hypens '-' so we don't need special cases for them
        text = text.replace('\xc2\xad', '-')

        # Repair words that are broken up with a hyphen
        text = text.replace('-\n', '')

        # join sentences broken up in multiple lines
        text = re.sub('([\w\',\-:;])\n(\w)', '\\1 \\2', text)

        # Remove empty lines, except for page numbers
        text = re.sub('(?<!\d)\n\n(?!\d+\n\n)', '', text)

        # Put each sentence on its own line
        text = re.sub('(\.|\?|\!) +([A-Z](?!\.))', '\\1\n\\2', text)

        with open(filename + '.out', 'w') as out_file:
            out_file.write(text)
            print('Done!')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        clean(sys.argv[1])
    else:
        print('Usage: split.py file.txt')