def precision(words, ground_truth):
    a, b = set(words), set(ground_truth)
    return len(a.intersection(b)) / len(a)

def recall(words, ground_truth):
    a, b = set(words), set(ground_truth)
    return len(a.intersection(b)) / len(b)

def jaccard_similarity(words, ground_truth):
    a, b = set(words), set(ground_truth)
    return len(a.intersection(b)) / len(a.union(b))

def average(thesaurus, ground_truth, function=precision):
    """
    Calculate the average of a metric over all words in the thesaurus
    Words that not in the ground truth thesaurus are not used
    They are reported seperately
    """
    not_included = 0
    cum_sum = 0
    for word in thesaurus:
        if word in ground_truth:
            cum_sum += function(thesaurus[word], ground_truth[word])
        else:
            not_included += 1
    result = cum_sum / (len(thesaurus) - not_included)
    return result, not_included
