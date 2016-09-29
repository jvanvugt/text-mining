"""
Text Mining week 5
Compute Cohen's kappa of 2 columns in a csv file

Author: Joris van Vugt
"""

import sys
import pandas as pd
import numpy as np

def kappa(pos_pos, pos_neg, neg_pos, neg_neg):
    """
    Compute Cohen's Kappa
    """
    total = pos_pos + pos_neg + neg_pos + neg_neg
    pr_a = (pos_pos + neg_neg) / total
    pr_yes1 = (pos_pos + pos_neg) / total
    pr_yes2 = (pos_pos + neg_pos) / total
    pr_e_yes = pr_yes1 * pr_yes2
    pr_e_no = (1-pr_yes1) * (1-pr_yes2)
    pr_e = pr_e_yes + pr_e_no
    k = (pr_a-pr_e) / (1-pr_e)
    return k

def analyze(filename, column_name1, column_name2):
    """
    Compute Cohen's Kappa of two columns of a csv file
    """
    data = pd.read_csv(filename)[[column_name1, column_name2]].dropna()

    positives = (data == 'P').as_matrix()
    pos_pos = positives.all(axis=1).sum()
    neg_neg = (~positives).all(axis=1).sum()
    pos_neg = np.logical_and(positives[:, 0], ~positives[:, 1]).sum()
    neg_pos = np.logical_and(positives[:, 1], ~positives[:, 0]).sum()
    print('\t P \t N')
    print('P \t {} \t {}'.format(pos_pos, pos_neg))
    print('N \t {} \t {}\n'.format(neg_pos, neg_neg))
    print('Cohens kappa={0:.2f}'.format(kappa(pos_pos, pos_neg, neg_pos, neg_neg)))

if __name__ == '__main__':
    if len(sys.argv) == 4:
        analyze(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print('Usage: sentiment_analysis.py file.csv column_name1 column_name2')
