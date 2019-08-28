# biGRU.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-10

# This script defines a function that trains a Bidirectional GRU neural net for
# each embedding and saves it in the models folder.

# USAGE:
'''
python src/models/biGRU.py \
--input_csv data/interim/train_2018-qualitative-data.csv \
--input_pk1 models/embed_matrices.pickle \
--input_pk2 data/processed/X_train_encoded.pickle \
--output1_h5 models/biGRU_glove_crawl.h5 \
--output2_h5 models/biGRU_glove_wiki.h5 \
--output3_h5 models/biGRU_fasttext_crawl.h5
'''

# Import Modules
import pickle
import pandas as pd
import numpy as np
from keras.layers import Dense, Input, Embedding
from keras.layers import Bidirectional, Conv1D
from keras.layers import GlobalMaxPooling1D, GlobalAveragePooling1D
from keras.layers import GRU, concatenate
from keras.models import Model
from keras import backend as K
K.set_learning_phase(1)
import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description='Build Conv1d Model')

    parser.add_argument('--input_csv', '-i', type=str, dest='input_csv',
                        action='store',
                        help='the input csv file with comments and labels')

    parser.add_argument('--input_pk1', '-i2', type=str, dest='input_pk1',
                        action='store',
                        help='the input embedding_matrix')

    parser.add_argument('--input_pk2', '-i3', type=str, dest='input_pk2',
                        action='store',
                        help='input encoded comments')

    parser.add_argument('--output1_h5', '-o', type=str,
                        dest='output1_h5', action='store',
                        help='the output biGRU gloveCrawl model')

    parser.add_argument('--output2_h5', '-o2', type=str,
                        dest='output2_h5', action='store',
                        help='the output biGRU glove Wiki model')

    parser.add_argument('--output3_h5', '-o3', type=str,
                        dest='output3_h5', action='store',
                        help='the output biGRU fasttext Crawl model')

    args = parser.parse_args()
    return args


def train_biGRU(X_train, Y_train, embed_name, embed_matrix):

    # Define parameters for Neural Net Architecture
    max_features = embed_matrix.shape[0]
    maxlen = 700
    batch_size = 128
    filters = 64
    kernel_size = 3
    epochs = 12
    embed_size = 300

    # Neural Net Architecture
    inp = Input(shape=(maxlen, ))

    x = Embedding(max_features, embed_size, weights=[embed_matrix],
                  trainable=False)(inp)

    x = Bidirectional(GRU(128, return_sequences=True, dropout=0.1,
                          recurrent_dropout=0.1))(x)
    x = Conv1D(filters, kernel_size=kernel_size, padding="valid",
               kernel_initializer="glorot_uniform")(x)

    avg_pool = GlobalAveragePooling1D()(x)
    max_pool = GlobalMaxPooling1D()(x)

    x = concatenate([avg_pool, max_pool])

    preds = Dense(12, activation="sigmoid")(x)

    model = Model(inp, preds)

    model.compile(loss='binary_crossentropy', optimizer='adam',
                  metrics=['accuracy'])

    # Train Model
    model.fit(X_train, Y_train, batch_size=batch_size,
              epochs=epochs, validation_split=0.15)

    return model


###############################################################################
if __name__ == "__main__":

    args = get_arguments()

    embed_names = ['glove_crawl', 'glove_wiki', 'fasttext_crawl']

    # Get labels
    df = pd.read_csv(args.input_csv)
    Y_train = np.array(df.loc[:, "CPD":"OTH"])

    # Load embedding matrices
    with open(args.input_pk1, 'rb') as handle:
        embed_matrices = pickle.load(handle)

    # Load training data
    with open(args.input_pk2, 'rb') as handle:
        X_train_encoded = pickle.load(handle)

    # Train biGRU models and save in the models folder
    biGRU_models = {}
    for embed in embed_names:
        print('Training biGRU on', embed, 'embedding')

        biGRU_models[embed] = train_biGRU(X_train_encoded[embed],
                                          Y_train, embed,
                                          embed_matrices[embed])

    biGRU_models['glove_crawl'].save(args.output1_h5)
    biGRU_models['glove_wiki'].save(args.output2_h5)
    biGRU_models['fasttext_crawl'].save(args.output3_h5)
