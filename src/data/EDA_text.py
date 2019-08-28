# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 11:24:21 2019

@author: payla
"""


import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

from wordcloud import WordCloud, STOPWORDS
stopwords = set(STOPWORDS)
import matplotlib.pyplot as plt


def word_frequency(text, max_features=200, min_df=10, ngram_range=(1, 1)):
    """
    Counts the word frequency in the given text
    
    Parameters
    ----------
    text: list
        The text to determine the word frequenies from
    max_features: int
        The max number of features for count vectorizer
    min_df: int
        The minimum frequency for a word to be added
    
    Returns
    -------
    Returns a data frame with the most frequent words and their counts
    
    """

    vect = CountVectorizer(min_df=min_df, 
                           max_features=max_features, 
                           stop_words="english",
                           ngram_range=ngram_range)
    term_doc_matrix = vect.fit_transform(text)
    words = vect.get_feature_names()

    word_counts = term_doc_matrix.sum(axis=0)
    word_count = []
    for i in word_counts.tolist():
        for j in i:
            word_count.append(j) 

    d = {"words":words, "counts":word_count}
    word_freq = pd.DataFrame(d)

    word_freq=word_freq.sort_values(by=["counts"], ascending=False)
    return word_freq

def generate_WordCloud(text, background_color="white", min_font_size=10, max_words=50, collocations=False,
                      width=800, height=800):
    """
    Creates a word cloud from the given text
    
    Parameters
    ----------
    text: str
        Input to the wordcloud
        
        
    Returns
    -------
    Returns the wordcloud as a matplotlib plot
    
    """
    
    
    wordcloud = WordCloud(width = width, 
                      height = height, 
                      background_color = background_color, 
                      stopwords = stopwords, 
                      min_font_size =  min_font_size, 
                      max_words=max_words,
                      collocations=collocations
                     ).generate(text) 

    plt.figure(figsize = (10, 10)) 
    plt.imshow(wordcloud) 
    plt.axis("off") 

    return plt.show() 



def sentence_eda(sentences, word_plot=False, character_plot=False):
    """
    Input list of sentences and get the mean, median, max, min number of words per sentence.
    The average mean, median, max and min number of characters per sentence.
    If plot = True, it outputs a histogram of the distribution of sentence length
    
    Parameters
    ----------
    sentences: list
        List of sentences to have words and characters
    word_plot: bool
        If true is selected it will show a plot of the distribution of the
        number of words per sentences. The default is set to False which means
        the plot will not display. 
    character_plot: bool
        If true is selected it will show a plot of the distribution of the
        number of characters per sentence. The default is set to False which means
        the plot will not display.
    
    Returns
    -------
    Displays word plot and character plot if selected and returns a dataframe with
    summary statistics.
    
    stats_df: dataframe
        Dataframe with the min, max, mean and median for the number of words and
        characters. 
   
    """
    # count the number of characters per sentence
    counts_char = []
    for chracters in sentences:
        counts_char.append(len(chracters))
    minimum_char = min(counts_char)
    maximum_char = max(counts_char)
    mean_char = np.mean(counts_char)
    median_char = np.median(counts_char)

    if character_plot == True:
        fig=plt.figure(figsize=(10, 6))
        plt.hist(counts_char, 50)
        plt.title("Number of characters per sentence", fontsize=16)
        plt.xlabel('Number of characters', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        plt.show();

    # count number of words per sentence
    counts_words = []
    for words in sentences:
        counts_words.append(len(words.split()))
    minimum_word = min(counts_words)
    maximum_word = max(counts_words)
    mean_word = np.mean(counts_words)
    median_word = np.median(counts_words)

    if word_plot == True:
         fig=plt.figure(figsize=(10, 6))
         plt.hist(counts_words, 40)
         plt.title("Number of words per sentence", fontsize=16)
         plt.xlabel('Number of words', fontsize=14)
         plt.ylabel('Count', fontsize=14)
         plt.show();

    # create lists for the dataframe
    labels = ["min", "max", "mean", "median"]
    values_char = [minimum_char, maximum_char, mean_char, median_char]
    values_word = [minimum_word, maximum_word, mean_word, median_word]
    # create dataframe
    d = {'stats' : labels,
         'character values': values_char,
         'word values': values_word}
    stats_df = pd.DataFrame(data=d).round(2)

    return stats_df


    
    
    