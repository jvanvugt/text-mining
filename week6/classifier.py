"""
Exercise week 6 of text mining
Predict sentiment of tweets containing #Trump

Author: Joris van Vugt
"""

import re

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, f1_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline

def load_data(filename):
    """
    Load the annotated data from a csv
    """
    data = pd.read_csv(filename, na_values='?')
    return data

def load_dictionary(filename):
    """
    Read in a list of words from a file
    """
    with open(filename) as f:
        return f.read().splitlines()

pos_words = load_dictionary('positive_words.txt')
pos_words.remove('trump')

neg_words = load_dictionary('negative_words.txt')

def maybe_replace(word, pos_token='<P>', neg_token='<N>'):
    """
    Return a token if the word is in the list of positive or negative words
    """
    for pos in pos_words:
        if word == pos:
            return pos_token

    for neg in neg_words:
        if word == neg:
            return neg_token

    return word

def preprocess(tweet):
    """
    Preprocess a tweet to reduce vocabulary size
    """
    # Remove hashtags and mentions
    tweet = tweet.replace('#', '').replace('@', '')
    # Split CamelCase into Camel Case
    tweet = re.sub('([a-z])([A-Z])', r'\1 \2', tweet)
    # Make lowercase and split into words
    tweet = tweet.lower().split()
    # Map all positive words and negative words into their
    # respective category
    tweet = ' '.join([maybe_replace(word) for word in tweet])  
    return tweet


def learn(data, **kwargs):
    """
    Use machine learning to predict tweet sentiments

    The data is split into 10 folds.
    Each fold is predicted by a naive bayes classifer
    trained on the other 9 folds.

    Return the predictions
    """
    k_fold = KFold(n_splits=10, shuffle=True)
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer(**kwargs)),
        ('tfidf', TfidfTransformer()),
        ('classifier', MultinomialNB()),
    ])

    X = data.Tweet.apply(preprocess)

    y = data.Annotation
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

    Return the predictions
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

def classify(classifier=learn, **kwargs):
    """
    Classify tweets using a given classifier method and
    print performance metrics of the classifier
    
    kwargs are passed to the classifier method

    Return the f1-score of the classifier
    """
    data = load_data('tweets.csv').dropna()
    data.Annotation = data.Annotation == 'P'
    predictions = classifier(data, **kwargs)
    ground_truth = data.Annotation.as_matrix()
    data['Prediction'] = predictions.astype(np.bool)
    data.to_csv('output.csv')

    targets = ['Negative', 'Positive']

    print(classification_report(
        ground_truth, predictions, target_names=targets))
    
    return f1_score(ground_truth, predictions, average='macro')
    

def grid_search():
    """
    Exhaustively try all combinations of (hardcoded)
    parameters

    The performance of each combination is averaged over 20 runs 
    """
    for n_gram in zip(range(1, 8), range(1, 8)):
        for analyzer in ('word', 'char', 'char_wb'):
            mean_f1 = np.array([classify(learn, ngram_range=n_gram, analyzer=analyzer) for _ in range(20)]).mean()
            print('n_gram: {}, analyzer: {} -> f1={}'.format(n_gram, analyzer, mean_f1))

if __name__ == '__main__':
    classify(classifier=learn)