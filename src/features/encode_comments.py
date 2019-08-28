# encode_comments.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-09

# This script encodes the comments for the Keras Model to train and predict
# Default inputs are set to encode the 2018 train comments

# For MakeFile do both usages
# USAGE for train data:
'''
python src/features/encode_comments.py \
--input_csv data/interim/train_2018-qualitative-data.csv \
--input_pk models/embed_tokenizers.pickle \
--output_pk data/processed/X_train_encoded.pickle
'''

# USAGE for test data
'''
python src/features/encode_comments.py \
--input_csv data/interim/test_2018-qualitative-data.csv \
--input_pk models/embed_tokenizers.pickle \
--output_pk data/processed/X_test_encoded.pickle
'''


# Import modules
import sys
sys.path.insert(1, '.')
import argparse
import pickle
import pandas as pd
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from src.data.preprocessing_text import preprocess_for_embed


def get_arguments():
    parser = argparse.ArgumentParser(description='Encode comments from csv to'
                                     'arrays with number representations')

    parser.add_argument('--input_csv', '-i', type=str, dest='input_csv',
                        action='store',
                        help='the input csv file with comments')

    parser.add_argument('--input_pk', '-i2', type=str, dest='input_pk',
                        action='store',
                        help='the input tokenizer')

    parser.add_argument('--output_pk', '-o', type=str,
                        dest='output_pk', action='store',
                        help='the output encoded comments')

    args = parser.parse_args()
    return args


def get_encoded_comments(comments, tokenizer, embed_name):

    comments = np.array(preprocess_for_embed(comments, embed_name, False))
    X = tokenizer.texts_to_sequences(comments)
    X = pad_sequences(X, maxlen=700)

    return X


###############################################################################
if __name__ == "__main__":

    args = get_arguments()
    embed_names = ['glove_crawl', 'glove_wiki', 'fasttext_crawl']
    df = pd.read_csv(args.input_csv)
    comments = df.iloc[:, 1]

    # Load Tokenizers
    with open(args.input_pk, 'rb') as handle:
        embed_tokenizers = pickle.load(handle)

    # Encode Comments and save processed data for model training
    encoded_comments = {}
    for embed in embed_names:
        encoded_comments[embed] = get_encoded_comments(comments,
                                                       embed_tokenizers[embed],
                                                       embed)

    with open(args.output_pk, 'wb') as handle:
        pickle.dump(encoded_comments, handle, protocol=pickle.HIGHEST_PROTOCOL)
