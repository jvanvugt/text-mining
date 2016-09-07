import sys
import re

def clean(filename):
    with open(filename, 'r') as file:
        # remove empty lines
        raw_text = ''.join(filter(lambda l: l != '\n', file.readlines()))

        # Put each sentence on its own line
        clean_text = re.sub('(\.|\?|\!)\s([A-Z])', '\\1\n\\2', raw_text)

        # repair words that are broken up with a hyphen
        clean_text = clean_text.replace('-\n', '')
        
        with open(filename + '.out', 'w') as out_file:
            out_file.write(clean_text)
            print('Done!')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        clean(sys.argv[1])
    else :
        print('Usage: split.py file.txt')