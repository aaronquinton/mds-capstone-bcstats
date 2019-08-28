# keras_embeddings.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-09

# This script prepares the tokenizer and embedding matrices for the
# Keras deep learning models. It saves a dictionary of tokenizers and a
# dictionary of arrays with an item for each embedding. These are saved in the
# models folder. To run this script you need to have the required pretrained
# embeddings in the reference folder. See Readme for more details

# USAGE:
'''
python src/features/keras_embeddings.py \
--input_csv data/interim/train_2018-qualitative-data.csv \
--input_embed_glove_crawl references/pretrained_embeddings.nosync/glove/glove.840B.300d.w2v.txt \
--input_embed_glove_wiki references/pretrained_embeddings.nosync/glove/glove.6B.300d.w2v.txt \
--input_embed_fasttext_crawl references/pretrained_embeddings.nosync/fasttext/crawl-300d-2M.vec \
--output_pk1 models/embed_tokenizers.pickle \
--output_pk2 models/embed_matrices.pickle
'''

# Import Modules
import sys
sys.path.insert(1, '.')
import pickle
import argparse
import pandas as pd
import numpy as np
from src.data.preprocessing_text import preprocess_for_embed
from keras.preprocessing.text import Tokenizer
from gensim.models import KeyedVectors


def get_arguments():
    parser = argparse.ArgumentParser(description='Get comment data to build'
                                     'tokenizers and embedding matrices')

    parser.add_argument('--input_csv', '-i', type=str, dest='input_csv',
                        action='store',
                        help='the input csv file with comments')

    parser.add_argument('--input_embed_glove_crawl', type=str,
                        dest='input_embed_glove_crawl',
                        action='store',
                        help='the input glove crawl embed')

    parser.add_argument('--input_embed_glove_wiki', type=str,
                        dest='input_embed_glove_wiki',
                        action='store',
                        help='the input glove wiki embed')

    parser.add_argument('--input_embed_fasttext_crawl', type=str,
                        dest='input_embed_fasttext_crawl',
                        action='store',
                        help='the input glove fasttext embed')

    parser.add_argument('--output_pk1', '-o1', type=str,
                        dest='output_pk1', action='store',
                        help='the output embed tokenizer')

    parser.add_argument('--output_pk2', '-o2', type=str,
                        dest='output_pk2', action='store',
                        help='the output embed matrix')

    args = parser.parse_args()
    return args


def get_embed_tokenizer(comments, embed_name, max_words=12000):

    comments = np.array(preprocess_for_embed(comments, embed_name, False))
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(comments)

    return tokenizer


def get_embed_matrix(embed_index, tokenizer, embed_size=300, max_words=12000):

    word_index = tokenizer.word_index
    num_words = min(max_words, len(word_index) + 1)
    embedding_matrix = np.zeros((num_words, embed_size), dtype='float32')

    for word, i in word_index.items():

        if i >= max_words:
            continue

        try:
            embedding_vector = embed_index[word]

            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector
        except:
            continue

    return embedding_matrix


###############################################################################
if __name__ == "__main__":

    args = get_arguments()

    # Default file paths for pre trained embeddings
    embedding_fnames = {
        'glove_crawl': args.input_embed_glove_crawl,
        'glove_wiki': args.input_embed_glove_wiki,
        'fasttext_crawl': args.input_embed_fasttext_crawl}

    embed_names = ['glove_crawl', 'glove_wiki', 'fasttext_crawl']

    df = pd.read_csv(args.input_csv)
    comments = df.iloc[:, 1]

    # Get and save tokenizers for each embedding
    # Preprocessing the comments is different depending on the embedding, which
    # is why there are different tokenizers
    embed_tokenizers = {}
    for embed in embed_names:
        embed_tokenizers[embed] = get_embed_tokenizer(comments, embed)

    with open(args.output_pk1, 'wb') as handle:
        pickle.dump(embed_tokenizers, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Load pretrained embeddings
    embed_indices = {}
    for embed in embedding_fnames.keys():
        print('Loading pretrained embedding for', embed)
        embed_indices[embed] = KeyedVectors.load_word2vec_format(
                                    embedding_fnames[embed],
                                    unicode_errors='ignore',
                                    binary=False)

    # Get and save the embedding matrix for each embedding
    embed_matrices = {}
    for embed in embedding_fnames.keys():
        embed_matrices[embed] = get_embed_matrix(embed_indices[embed],
                                                 embed_tokenizers[embed])

    with open(args.output_pk2, 'wb') as handle:
        pickle.dump(embed_matrices, handle, protocol=pickle.HIGHEST_PROTOCOL)
