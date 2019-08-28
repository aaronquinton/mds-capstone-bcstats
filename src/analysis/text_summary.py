# -*- coding: utf-8 -*-
"""
text_summary.py
Aaron Quinton, Ayla Pearson and Fan Nie
June 2019

This script preforms text summarization. The generate_text_summary combines
all the functions into a single step. The general workflow if you wanted to
break the analysis up is as follows:

1. Load the data
2. Clean up grammar to make comments split into more evenly sized sentences
3. pre-process the text to remove punctutation and stopwords
4. Create the corpus from individual comments
5. Generate the summary

Usage
-----
This file can be imported as python module and all funtions can be used:

    Example:
    `from src.analysis.text_summary import generate_text_summary`

The generate_text_summary function can be called from the command line
as a script:

    Example:
    python -m src.analysis.text_summary .\data\interim\joined_qual_quant.csv
    ./references/data-dictionaries/theme_subtheme_names.csv 200 theme
    Supervisors strong textrank


"""

import re                         # Version 2.2.1
import numpy as np                # Version 1.16.2
import pandas as pd               # Version 0.23.4
import matplotlib.pyplot as plt   # Version 3.0.2
import nltk                       # Version 3.4
import argparse                   # Version 1.1


from src.data.preprocessing_text import clean_text
from src.data.preprocessing_text import replace_typical_misspell

from gensim.models import KeyedVectors                  # Version 3.7,1
import networkx as nx                                   # Version 2.2
from sklearn.metrics.pairwise import cosine_similarity  # Version 0.20.1

from gensim.summarization.summarizer import summarize as gensim_summarize
# Version 3.7.1



def generate_corpus_from_comments(data, depth=None, name=None, agreement=None,
                            sentences=True):
    """
    Filters the data frame down to a specific subtopic or topic and agreement
    level. If all the defaults are used it will generate a corpus for all the
    comments present. It also cleans up the grammar in the text so it more
    evenly splits into sentences.

    Parameters
    ----------
    data: dataframe
        Dataframe with the columns USERID, theme, code, text and diff present
        if you are looking at agreement levels.
    depth: str
        Either "theme" or "subtheme" or None. The default is none
        which will give counts for all comments. To use name or agreement
        this can not be set to None.
    name: str or integer
        Either input the name of the main theme (ex: "Executive",
        "Staffing Practices") or the number relating to the subtheme
        (ex: 12, 43, 102). The default is None which means it will do all the
    agreement: str
        Either input "all" to see all three levels together or input the level
        of agreement "strong", "weak", "no". Default is set to None which is for
        comments that have not be related to the multiple choice questions
    sentences: bool
        This either leaves the corpus as a single string or breaks it into
        sentences. The default is true which breaks it into sentences

    Returns
    -------
    Returns the combined comments as either a list or string depending on the
    sentences parameters.

    sentences: list
        Returns all the combined comments as a list, where each comment is an
        item in the list. To have the function return this format select True
        for the sentences parameter.
    text: str
        Returns all the combined comments as a sinlge string. To have it
        returned in this form have the sentences parameter False.

    """

    data = data.copy()
    # filter to either theme or subtheme level
    if depth == "theme":
        if name not in data['theme'].unique():
            raise TypeError("theme not present in data")
        data = data[data["theme"] == name]
    if depth == "subtheme":
        if name not in data['code'].unique():
            raise TypeError("subtheme not present in data")
        data = data[data["code"] == name]

    possible_agreements = ["strong", "weak", "no", "all", None]
    if agreement not in possible_agreements:
        raise TypeError("Entered wrong agreement level must be 'strong'," +
        "'weak' 'no', 'all', None")

    # filter when agreement level is present
    if agreement != None:
        agreement_dict = {"strong":0, "weak":1, "no":0}
        agreement_level = agreement_dict[agreement]
        data = data[data["diff"] == agreement_level]

    # remove duplicate comments
    data = data.drop_duplicates(subset=['USERID'])
    # add each comment to a list
    text = []
    for comment in data["text"]:
        text.append(comment)
    # combine list to be a single item
    text = ' '.join(text)

    if sentences == True:
        text = corpus_clean_sentences(text)
        sentences = nltk.sent_tokenize(text)
        return sentences

    if sentences == False:
        text = corpus_clean_sentences(text)
        return text


def corpus_clean_sentences(text):
    """
    Takes a string and cleans the grammar so it will more evenly split
    into sentences.

    Parameters
    ----------
    text: str
        Text to be cleaned

    Returns
    -------
    Returns string that is ready for sentence tokenization

    """

    # change semi-colon (;) to .
    text = re.sub(r';', '.', text)
    # change * to no space
    text = re.sub(r'\*', '', text)
    # if more then 3 spaces add .
    text = re.sub(r'   ', '.', text)
    # change all ... to ' '
    text = re.sub(r'\.{3}', ' ', text)
    # change i.e. to ie
    text = re.sub(r'i\.e\.', 'ie', text)
    # change i.e. to ie
    text = re.sub(r'Ie\.', 'ie', text)
    # change etc. to etc
    text = re.sub(r'etc\.', 'etc', text)
    # change e.g. to eg
    text = re.sub(r'e\.g\.', 'eg', text)
    # change E.g. to eg
    text = re.sub(r'E\.g\.', 'eg', text)
    # change E.g. to eg
    text = re.sub(r'eg\.', 'eg', text)
    # any sentences that have .words change to . words or, words
    text = re.sub(r'([\.,])(\S)', r'\1 \2', text)
    # change - to .
    ## this will cause some poor text
    ## but overall it will split up really long sentences
    text = re.sub(r'\s-\s', '. ', text)
    # remove double spaces
    text = re.sub(r'  ', ' ', text)
    # remove all 1) etc
    text = re.sub(r'\d\)', '', text)
    # change any . . to .
    text = re.sub(r'\.\s\.', '. ', text)
    # change any ' '-
    text = re.sub(r'(\s-)', ' ', text)
    # change ADM to adm because it was not splitting on ADM.
    # slightly ugly because adds an extra . but splits it now
    text = re.sub(r'ADM\.', 'ADM. .', text)
    # remove all 1. etc
    text = re.sub(r'\d\.', '', text)

    return text



def preprocess_corpus(text, stop_words=""):
    """
    Preprocesses the text for the fastText crawl pretrained embeddings.
    It removes all puncuation, fixes spelling to match vocab and removes
    stop words.

    Parameters
    ----------
    text: list
        List containing each sentence as an item
    stop_words: list or default
        If default selected a stop word list is supplied otherwise you
        can pass it your own

    Returns
    -------
    Returns preprocessed sentences in a list

    """

    if stop_words == "":
        stop_words = ["a", "an", "to", "of", "and", "it"]

    preprocessed = []
    for sentence in text:
        # removes all puncuation
        x = clean_text(sentence)
        # fix spelling
        x = replace_typical_misspell(x)
        # remove stop words
        sentence_no_stopwords = []
        for word in x.split():
            if word not in stop_words:
                sentence_no_stopwords.append(word)
        processed_sentences = " ".join(sentence_no_stopwords)
        preprocessed.append(processed_sentences)

    return preprocessed


def load_word_embeddings(file_path):
    """
    Returns the loaded embeddings from the downloaded file

    Parameters
    ----------
    file_path: str
        The file path to the downloaded embeddings
    Returns
    -------
    loaded_embedding: gensim.models.keyedvectors.Word2VecKeyedVectors
        Returns the embeddings loaded as a gensim object

    """

    loaded_embedding = KeyedVectors.load_word2vec_format(file_path)
    return loaded_embedding



def generate_summary_pagerank_pretrained_embedding(text, embedding,
                                            embedding_size=300, size_summary=5):
    """
    Uses pre-trained word embeddings to get the average sentence embedding. The
    similarity between each sentence is calculated and stored in a graph.
    PageRank is then used to determine the most relavent sentences.

    # Reference https://www.analyticsvidhya.com/blog/2018/11/introduction-text-
    summarization-textrank-python/
    # some changes to the code from the blog

    Parameters
    ----------
    text: list
        Orginal form of the sentences which is used in the output of the summary
        so it is readable text compared to preprocessed text
    embedding: gensim.models.keyedvectors.Word2VecKeyedVectors
        Embeddings
    embedding_size: int
        The size of the word vectors. The default is 300.
    size_summary: int
        The number of sentences to be included in the summary.

    Returns
    -------
    Returns a list with the top ranked sentences

    """
    # pre-process the text into sentences ready to be compared
    clean_sentences = preprocess_corpus(text)
    # get the average embedding for each sentence
    sentence_vectors = []
    for sentence in clean_sentences:
        # check if there is a sentence and make sure its not "" or " "
        if len(sentence) != 0:

            single_sentence_vect =[]
            for word in sentence.split():
                # need excpetion handling incase word not in the embedding
                # generates a np.array with all zeros
                try:
                    w = embedding[word]
                except:
                    w = np.zeros((embedding_size,))
                # create vector of all words in a sentence
                single_sentence_vect.append(w)
            # get the average embedding for the sentence
            v = sum(single_sentence_vect)/(len(sentence.split()))
        # if the sentence is blank just give it all zeros
        else:
            v = np.zeros((embedding_size,))
        sentence_vectors.append(v)

           # similarity matrix
    sim_mat = np.zeros([len(text), len(text)])
    # add cosine similarity scores to the matrix
    for i in range(len(text)):
        for j in range(len(text)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,
                embedding_size), sentence_vectors[j].reshape(1,
                embedding_size))[0,0]

    # create graph from cosine matrix: nodes represent sentences
    # edges represent similarity scores between sentences
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)
   # sort by score
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(text)),
                                        reverse=True)
    # output top n sentences
    top_n = []
    for i in range(size_summary):
        top_n.append(ranked_sentences[i][1])
    return top_n


def generate_summary_gensim(text, size_summary=200):
    """
    Performs text summary from gensim summarizer

    Parameters
    ----------
    text: list
        A list of sentences

    Returns
    -------
    summary: list
        List with each item being a single sentence

    """
    text = preprocess_corpus(text)
    text = ". ".join(text)
    return gensim_summarize(text, word_count=size_summary, split=True)


def generate_text_summary(input_file, summary_size, depth, name, agreement,
                  method, embedding_file=None, embedding=None,
                  embedding_return=False, output_file="./data/processed/"):
    """
    Input the data file and this function will clean, process and summarize the
    comments. This funcation can summarize all the text or it split to
    subtheme/theme and agreement level. It will also generate an output file of
    a csv with the summary sentences.

    This function can perform text sumarization with different algorithms one
    using PageRank and the other using TextRank. The method can be choosen under
    the methods parameter.

    The pagerank method has been implemented locally and all the code is present
    in this module. This method is much slower, it has been included still
    because all the code is in the module and can be easily understood. To use
    this method you can save the loaded embeddings after the first time it has
    been run if you select the correct parameters. This can greatly decrease the
    time it takes to run. Examples are present below.

    The textrank method is from the Gensim package. It uses a variation on
    textrank where the similarity method is using BM25 similarity. Since this
    implementation is from a package the code is not present in this module.

    Parameters
    ----------
    input_file: str
        Path to the input data
    summary_size:
        For pretrained embedding it is the number of sentences
        For summa and gensim it is the number of characters
    depth: str
        Either theme, subtheme or None
    name: str or integer
        Either input the name of the main theme (ex: "Executive",
        "Staffing Practices") or the number relating to the subtheme
        (ex: 12, 43, 102). The default is None which means it will do all the
    agreement: str
        Either input "all" to see all three levels together or input the level
        of agreement "strong", "weak", "no". Default is set to None which is for
        comments that have not be related to the multiple choice questions
    method: str
        Select the summarization method to be used: "pagerank" or "textrank".
        The pagerank method uses pre-trained embeddings and is a slower method
        then textrank.
    output_file: str
        Path to where the summary file will be written out too. The default
        writes a file to the processed folder within data. If None is choosen
        then it will not write a file.
    embedding_file: str
        Path to the file containing the word embeddings
    embedding: gensim.models.keyedvectors.Word2VecKeyedVectors
        Loaded word vectors, this can help to save time once you have loaded
        them embeddings
    embedding_return: bool
        If set to true the function will return the loaded embeddings. It will
        still output the summary.

    Returns
    -------
    It prints the summary to screen and returns it. If embedding_return is true
    it also returns the loaded embedding.

    Summary: list
        the items are the sentence
    embedding: gensim.models.keyedvectors.Word2VecKeyedVectors
        If embedding_return == True it returns the summary and the loaded vector

    Examples
    --------
    # load and save the pretrained embeddings
    # geneate summary with 5 sentences for subtheme 13 with weak agreement
    summary, loaded_embedding = generate_text_summary(".\data\interim\
                                        linking_joined_qual_quant.csv",
                                        5,
                                        "subtheme",
                                        13,
                                        "weak",
                                        "pagerank",
                                        "./references/pretrained_embeddings.
                                        nosync/fasttext/crawl-300d-2M.vec",
                                        embedding_return=True)

    # now use the loaded embeddings to speed up the run time
    generate_text_summary(".\data\interim\linking_joined_qual_quant.csv",
                                    5,
                                    "subtheme",
                                    13,
                                    "weak",
                                    "pagerank",
                                    embedding=loaded_embedding)

    # to generate a summary with 200 characters for subtheme 13 with
    # weak agreement
    generate_text_summary(".\data\interim\linking_joined_qual_quant.csv",
                                        200,
                                        "subtheme",
                                        13,
                                        "weak",
                                        "textrank")

    # generate a summary 100 characters long for theme Supervisors with
    # strong agreement
    generate_text_summary(".\data\interim\linking_joined_qual_quant.csv",
                                        100,
                                        "theme",
                                        Supervisors,
                                        "strong",
                                        "textrank")

    # generate a summary 100 characters long for theme Supervisors with
    # strong agreement but choose to not have it write  a csv
    generate_text_summary(".\data\interim\linking_joined_qual_quant.csv",
                                        100,
                                        "theme",
                                        Supervisors,
                                        "strong",
                                        "textrank",
                                        output_file=None)

    """
    # read in data and legend
    data = pd.read_csv(input_file)
    # generate corpus
    corpus = generate_corpus_from_comments(data,
                                           depth=depth,
                                           name=name,
                                           agreement=agreement,
                                           sentences=True)

    if method not in ["pagerank", "textrank"]:
        raise TypeError("incorrect method selected")
    # PageRank with word embeddings
    if method == "pagerank":
        if isinstance(embedding_file, str) == True:
            print("loading embeddings, this will take a few mins")
            # load embeddings
            embedding_tr = load_word_embeddings(embedding_file)
            embed = embedding_tr
        if embedding != None:
            embed = embedding
        # generate summary
        summary = generate_summary_pagerank_pretrained_embedding(corpus,
                                                    embed,
                                                    embedding_size=300,
                                                    size_summary=summary_size)
    if method == "textrank":
        corpus_preprocess = preprocess_corpus(corpus)
        summary_processed = generate_summary_gensim(corpus_preprocess,
                                                        summary_size)
        # match sentences to original corpus so summary is more readable
        # (ie contains stopwords)
        summary = []
        for sentence in summary_processed:
            processed = re.sub(r'\.', '', sentence)
            index = corpus_preprocess.index(processed)
            summary.append(corpus[index])

    if depth == None:
        if agreement == None:
            title = "Summary for 2018 WES"
        else:
            title = "Summary for 2018 WES"  +\
            " - " + str(agreement).title() +" Agreement"
    if depth == "subtheme":
        if agreement == None:
            title = "Summary for " +\
            str(data[data["code"] == name].iloc[0]["subtheme_description"]).title()
        else:
            title = "Summary for " +\
            str(data[data["code"] == name].iloc[0]["subtheme_description"]).title()  +\
            " - " + str(agreement).title() +" Agreement"
    if depth == "theme":
        if agreement == None:
            title = "Summary for " + str(name).title()
        else:
            title = "Summary for " + str(name).title() + " - "  +\
            str(agreement).title() +" Agreement"

    # print summary to screen
    print(title)
    print("-------------------------------------------------------------------")
    for i in summary:
        print(i, "\n")

    if output_file != None:
        output_file_with_name = output_file + "summary_" + str(name) + ".csv"
        df_write = pd.DataFrame(summary, columns=["summary"])
        df_write["theme/subtheme"] = name
        df_write.to_csv(output_file_with_name, index=False)

    if embedding_return == True:
        return summary, embedding_tr

    return summary



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    parser.add_argument("summary_size", type=int)
    parser.add_argument("depth", type=str)
    parser.add_argument("name", type=str)
    parser.add_argument("agreement", type=str)
    parser.add_argument("method", type=str)
    parser.add_argument("--embedding_file", default=None)
    parser.add_argument("--embedding", default=False)
    parser.add_argument("--embedding_return", default=False)
    parser.add_argument("--output_file", default="./data/processed/")
    args = parser.parse_args()

    generate_text_summary(args.input_file,
                          args.summary_size,
                          args.depth,
                          args.name,
                          args.agreement,
                          args.method,
                          embedding_file=args.embedding_file,
                          embedding=args.embedding,
                          embedding_return=args.embedding_return,
                          output_file=args.output_file)
