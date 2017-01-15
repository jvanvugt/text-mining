import sys
import pickle

import matplotlib.pyplot as plt
plt.style.use('ggplot')

def precision(words, ground_truth):
    a, b = set(words), set(ground_truth)
    return len(a.intersection(b)) / len(a)

def recall(words, ground_truth):
    a, b = set(words), set(ground_truth)
    return len(a.intersection(b)) / len(b)

def jaccard_similarity(words, ground_truth):
    a, b = set(words), set(ground_truth)
    return len(a.intersection(b)) / len(a.union(b))

def average(thesaurus, ground_truth, function=precision, n=None):
    """
    Calculate the average of a metric over all words in the thesaurus
    Words that not in the ground truth thesaurus are not used
    They are reported seperately
    """
    not_included = 0
    cum_sum = 0
    for word in thesaurus:
        if word in ground_truth and len(ground_truth[word]) != 0:
            words = thesaurus[word]
            if n is not None:
                words = words[:n]
            cum_sum += function(words, ground_truth[word])
        else:
            not_included += 1
    result = cum_sum / (len(thesaurus) - not_included)
    return result, not_included


def compute_stats(ths_file, gt_file, n=20):
    with open(ths_file, 'rb') as tf, open(gt_file, 'rb') as gtf:
        thesaurus = pickle.load(tf)
        ground_truth = pickle.load(gtf)
    
    recalls, precisions = [], []
    for i in range(1, 20):
        recall_n, _ = average(thesaurus, ground_truth, function=recall, n=i)
        prec_n, _ = average(thesaurus, ground_truth, function=precision, n=i)
        recalls.append(recall_n)
        precisions.append(prec_n)
    
    print('Recalls:')
    print(recalls)
    print('\n\nPrecisions:')
    print(precisions)

    plt.plot(recalls, precisions)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall curve')
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python {} thesaurus ground_truth'.format(__file__))
    else:
        compute_stats(sys.argv[1], sys.argv[2])