"""
Exercise week 6 of text mining
Predict sentiment of tweets containing #Trump

Author: Joris van Vugt
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline

def load_data(filename):
    """
    Load the annotated data from a csv
    """
    data = pd.read_csv(filename, na_values='?')
    print(data.Annotation.value_counts())
    return data

def load_dictionary(filename):
    """
    Read in a list of words from a file
    """
    with open(filename) as f:
        return f.read().splitlines()

def learn(data):
    """
    Use machine learning to predict tweet sentiments

    The data is split into 10 folds.
    Each fold is predicted by a naive bayes classifer
    trained on the other 9 folds.
    """
    k_fold = KFold(n_splits=10, shuffle=True)
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer(ngram_range=(7, 7), analyzer='char')),
        ('tfidf', TfidfTransformer()),
        ('classifier', MultinomialNB()),
        ])

    X, y = data.Tweet, data.Annotation
    predictions = np.empty(len(y))
    for train_idx, test_idx in k_fold.split(X, y):
        pipeline.fit(X.iloc[train_idx], y.iloc[train_idx])
        predictions[test_idx] = pipeline.predict(X.iloc[test_idx])

    return predictions
        

def naive_wordcount(data, prior=True):
    """
    Naive classification method based on dictionaries
    of positive and negative words

    The tweet will be classified based on whether it
    contains mostly positive or negative words

    If the number of positive and negative words are equal,
    the tweet is assigned the prior.
    """
    pos_words = load_dictionary('positive_words.txt')
    neg_words = load_dictionary('negative_words.txt')

    predictions = []
    for tweet in data.Tweet:
        # Make the tweet all lowercase, remove # symbols
        # and split it into words
        words = tweet.lower().replace('#', '').split()
        
        # Count positive and negative words
        n_pos = np.array([word in pos_words for word in words]).sum()
        n_neg = np.array([word in neg_words for word in words]).sum()

        # Classify tweet
        if n_pos == n_neg:
            predictions.append(prior)
        else:
            predictions.append(n_pos > n_neg)

    return predictions

def classify(classifier=naive_wordcount, **kwargs):
    """
    Classify tweets using a given classifier method and
    print performance metrics of the classifier
    
    kwargs are passed to the classifier method
    """
    data = load_data('tweets.csv').dropna()
    data.Annotation = data.Annotation == 'P'
    predictions = classifier(data, **kwargs)
    ground_truth = data.Annotation.as_matrix()

    print('Precision:', precision_score(ground_truth, predictions))
    print('Recall:', recall_score(ground_truth, predictions))
    print('F1:', f1_score(ground_truth, predictions))


if __name__ == '__main__':
    classify(classifier=learn)