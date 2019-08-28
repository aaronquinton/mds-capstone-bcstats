# theme_classification.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-09

# This script predicts the theme on the test data for every model

# USAGE:

'''
python src/models/theme_classification.py \
--input_pk1 models/linearsvc_model.pickle \
--input_pk2 data/processed/X_test_encoded.pickle \
--input_npz data/processed/X_test_bow.npz \
--input1_h5 models/conv1d_models.h5 \
--input2_h5 models/biGRU_glove_crawl.h5 \
--input3_h5 models/biGRU_glove_wiki.h5 \
--input4_h5 models/biGRU_fasttext_crawl.h5 \
--output_pk data/output/test_predictions.pickle
'''

import sys
sys.path.insert(1, '.')
import pickle
import numpy as np
import pandas as pd
import scipy.sparse
import argparse
from keras.models import load_model


def get_arguments():
    parser = argparse.ArgumentParser(description='Get test predictions')

    parser.add_argument('--input_pk1', '-i1', type=str, dest='input_pk1',
                        action='store',
                        help='the input linearsvc model')

    parser.add_argument('--input_pk2', '-i2', type=str, dest='input_pk2',
                        action='store',
                        help='input encoded comments')

    parser.add_argument('--input_npz', '-i3', type=str, dest='input_npz',
                        action='store',
                        help='input bow comments')

    parser.add_argument('--input1_h5', '-i4', type=str,
                        dest='input1_h5', action='store',
                        help='the conv1d model')

    parser.add_argument('--input2_h5', '-i5', type=str,
                        dest='input2_h5', action='store',
                        help='the output biGRU gloveCrawl model')

    parser.add_argument('--input3_h5', '-i6', type=str,
                        dest='input3_h5', action='store',
                        help='the output biGRU glove Wiki model')

    parser.add_argument('--input4_h5', '-i7', type=str,
                        dest='input4_h5', action='store',
                        help='the output biGRU fasttext Crawl model')

    parser.add_argument('--output_pk', '-o', type=str,
                        dest='output_pk', action='store',
                        help='the output test predictions')

    args = parser.parse_args()
    return args


args = get_arguments()

##############################################################################
# Predict test data themes with Baseline BOW and Linear SVC Model
# Load Vectorized comments
X_text_bow = scipy.sparse.load_npz(args.input_npz)

# Load Linear SVC Model
with open(args.input_pk1, 'rb') as handle:
    linearsvc_model = pickle.load(handle)

# Predict themes
Y_bow = linearsvc_model.predict(X_text_bow)


###############################################################################
# Predict test data labels with Conv1d and biGRU Models
# Load Encoded Comments
with open(args.input_pk2, 'rb') as handle:
    X_test_encoded = pickle.load(handle)

# Load Neural Net Classification Models
conv1d = load_model(args.input1_h5)
biGRU_glove_crawl = load_model(args.input2_h5)
biGRU_glove_wiki = load_model(args.input3_h5)
biGRU_fasttext_crawl = load_model(args.input4_h5)

ensemble = (conv1d.predict(X_test_encoded['glove_wiki'])
            + biGRU_glove_crawl.predict(X_test_encoded['glove_crawl'])
            + biGRU_glove_wiki.predict(X_test_encoded['glove_wiki'])
            + biGRU_fasttext_crawl.predict(X_test_encoded['fasttext_crawl']))/4

###############################################################################
# Save test data predictions
Y_pred = {}
Y_pred['BOW'] = Y_bow
Y_pred['ensemble'] = ensemble

with open(args.output_pk, 'wb') as handle:
    pickle.dump(Y_pred, handle, protocol=pickle.HIGHEST_PROTOCOL)
