import sys
import re

if __name__ == '__main__':
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        with open(filename, 'r') as file:
            raw_text = ''.join(filter(lambda l: l != '\n', file.readlines()))
            clean_text = re.sub('(\.|\?|\!)\s', '\\1\n', raw_text)
            clean_text = clean_text.replace('-\n', '')
            with open(filename + '.out', 'w') as out_file:
                out_file.write(clean_text)
                print('Done!')
    else :
        print('Usage: split.py file.txt')