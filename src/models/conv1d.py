# conv1d.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-09

# This script defines a function that trains a convulutional neural net for
# each embedding and saves it in the models folder.

# USAGE:
'''
python src/models/conv1d.py \
--input_csv data/interim/train_2018-qualitative-data.csv \
--input_pk1 models/embed_matrices.pickle \
--input_pk2 data/processed/X_train_encoded.pickle \
--output_h5 models/conv1d_models.h5
'''

# Import Modules
import pickle
import pandas as pd
import numpy as np
from keras.layers import Dense, Embedding, Dropout, Activation
from keras.layers import GlobalMaxPooling1D, Conv1D
from keras.models import Sequential
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

    parser.add_argument('--output_h5', '-o', type=str,
                        dest='output_h5', action='store',
                        help='the output conv1d model')

    args = parser.parse_args()
    return args


def train_conv1d(X_train, Y_train, embed_name, embed_matrix):

    # Define parameters for Neural Net Architecture
    max_features = embed_matrix.shape[0]
    maxlen = 700
    batch_size = 128
    filters = 250
    kernel_size = 3
    hidden_dims = 250
    epochs = 7
    embed_size = 300

    # Neural Net Architecture
    model = Sequential()

    model.add(Embedding(max_features, embed_size, weights=[embed_matrix],
                        trainable=False, input_length=maxlen))

    model.add(Dropout(0.2))
    model.add(Conv1D(filters, kernel_size, padding='valid', activation='relu',
                     strides=1))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(hidden_dims))
    model.add(Dropout(0.2))
    model.add(Activation('relu'))
    model.add(Dense(12))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam',
                  metrics=['accuracy'])

    # Train Model
    model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs,
              validation_split=0.15)

    return model


###############################################################################
if __name__ == "__main__":

    args = get_arguments()

    embed = 'glove_wiki'

    # Get labels
    df = pd.read_csv(args.input_csv)
    Y_train = np.array(df.loc[:, "CPD":"OTH"])

    # Load embedding matrices
    with open(args.input_pk1, 'rb') as handle:
        embed_matrices = pickle.load(handle)

    # Load training data
    with open(args.input_pk2, 'rb') as handle:
        X_train_encoded = pickle.load(handle)

    # Train Conv1d models and save in the models folder
    print('Training conv1d on', embed, 'embedding')
    conv1d_model = train_conv1d(X_train_encoded[embed], Y_train, embed,
                                embed_matrices[embed])

    conv1d_model.save(args.output_h5)
