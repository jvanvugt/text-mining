"""
Author: Joris van Vugt

Preprocess an XML file from rechtspraak.nl
"""
import glob
import re
import time
import os
import multiprocessing
import ntpath

import frog


def sec_to_string(seconds):
    """
    Convert seconds to HH:MM:SS string
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

def lemmatize(sentence, frogger):
    """
    Convert each word in a sentence to its lemma
    """
    lemmas = [token['lemma'] for token in frogger.process(sentence)]
    return ' '.join(lemmas)

def preprocess(files):
    """
    Preprocess a list of XML-files
    The cleaned files will be saved in the output folder

    Remove the XML-tags and clean the remaining raw text
    to have one sentence per line with lemmatized words
    """
    frog_options = frog.FrogOptions(tok=False, morph=False, mwu=True,
                                    chunking=False, ner=False, numThreads=8)
    frogger = frog.Frog(frog_options, '/vol/customopt/lamachine/etc/frog/frog.cfg')

    start_time = time.time()
    for i, file_name in enumerate(files):
        outfile = ntpath.basename(file_name)[:-4] + '.txt'
        out_name = os.path.join(OUTPUT_FOLDER, outfile)
        if os.path.isfile(out_name):
            print('Already done:', out_name)
            continue
        with open(file_name, 'r', encoding='utf-8') as file:
            try:
                text = file.read()
                # Remove all XML tags
                text = re.sub('<[^>]*>', '', text)
                lines = text.splitlines()
                # Remove abundant whitespace
                lines = [line.strip() for line in lines]
                # One sentence per line
                lines = [re.sub(r'(\w)\. ([A-Z])', '\\1.\n\\2', line)
                         for line in lines]
                # Remove punctuation
                lines = [re.sub(r'[\.,:;/\(\)\[\]\'\"]', '', line)
                         for line in lines]
                # Remove empty lines and make lower case
                lines = [line.lower() for line in lines if line != '']
                # Convert each word to its lemma
                lemmas = [lemmatize(line, frogger) for line in lines]
                # Change extension to .txt
                with open(out_name, 'w', encoding='utf-8') as out:
                    out.write('\n'.join(lemmas))
                if i % 49 == 0 and i != 0:
                    print('Done {}/{}'.format(i, len(files)))
                    time_per_doc = (time.time() - start_time) / i
                    print('Average time/document:', sec_to_string(time_per_doc))
                    time_remaining = time_per_doc * (len(files) - i)
                    print('Time remaining:', sec_to_string(time_remaining))
            except UnicodeError:
                print('Skipping {}, UnicodeError'.format(file_name))

if __name__ == '__main__':
    s = time.time()
    INPUT_FOLDER = '/scratch/jvvugt/raw'
    OUTPUT_FOLDER = '/scratch/jvvugt/processed'
    n_jobs = 4
    print('CPU Count: ', multiprocessing.cpu_count())
    print('n_jobs:', n_jobs)

    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    files = glob.glob(INPUT_FOLDER + '/*.xml')
    n_files = len(files)
    print('%d files found in %s' % (n_files, INPUT_FOLDER))
    print('Writing to', OUTPUT_FOLDER)
    # multiprocessing
    pool = multiprocessing.Pool(n_jobs)
    # Split files into evenly sized chunks
    chunksize = round(n_files / n_jobs)
    file_chunks = [files[i:i+chunksize] for i in range(0, n_files, chunksize)]
    try:
        pool.map(preprocess, file_chunks)
    finally:
        pool.close()
        pool.join()
    print((time.time()-s))
