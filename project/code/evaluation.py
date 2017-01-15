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


def compute_stats(ths_file1, ths_file2, gt_file, n=20):
    with open(ths_file1, 'rb') as tf1, \
            open(ths_file2, 'rb') as tf2, \
            open(gt_file, 'rb') as gtf:
        th1 = pickle.load(tf1)
        th2 = pickle.load(tf2)
        ground_truth = pickle.load(gtf)

    r1, r2, p1, p2 = [], [], [], []
    for i in range(1, 20):
        r1.append(average(th1, ground_truth, function=recall, n=i)[0])
        r2.append(average(th2, ground_truth, function=recall, n=i)[0])
        p1.append(average(th1, ground_truth, function=precision, n=i)[0])
        p2.append(average(th2, ground_truth, function=precision, n=i)[0])
    
    for a in r1, r2, p1, p2:
        print(a)

    plt.plot(r1, p1, label='Word2Vec')
    plt.plot(r2, p2, label='LSA')
    plt.legend()
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python {} thesaurus1 thesaurus2 ground_truth'.format(__file__))
    else:
        compute_stats(sys.argv[1], sys.argv[2], sys.argv[3])
