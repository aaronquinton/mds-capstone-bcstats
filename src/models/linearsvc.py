# linearsvc.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-09

# This script file is for building the LinearSVC model

# USAGE for train data:
'''
python src/models/linearsvc.py \
--input_csv data/interim/train_2018-qualitative-data.csv \
--input_npz data/processed/X_train_bow.npz \
--output_pk models/linearsvc_model.pickle
'''

# Import Modules
import pandas as pd
import numpy as np
import scipy.sparse
from skmultilearn.problem_transform import BinaryRelevance
from sklearn.svm import LinearSVC
import pickle
import argparse


# Default filepath
filepath_in = './data/interim/train_2018-qualitative-data.csv'
filepath_in2 = 'data/processed/X_train_bow.npz'
filepath_out = 'models/linearsvc_model.pickle'


def get_arguments():
    parser = argparse.ArgumentParser(description='Build linearsvc model')

    parser.add_argument('--input_csv', '-i', type=str, dest='input_csv',
                        action='store', default=filepath_in,
                        help='the input csv file with comments and labels')

    parser.add_argument('--input_npz', '-i2', type=str, dest='input_npz',
                        action='store', default=filepath_in2,
                        help='the input csv file with comments and labels')

    parser.add_argument('--output_pk', '-o', type=str, dest='output_pk',
                        action='store', default=filepath_out,
                        help='the linear svc model')

    args = parser.parse_args()
    return args


def train_linearsvc(X_train, Y_train):

    model_bow = BinaryRelevance(
        classifier=LinearSVC(C=0.5, tol=0.2)
    )

    model_bow.fit(X_train, Y_train)

    return model_bow


###############################################################################
if __name__ == "__main__":

    args = get_arguments()

    # Get labels
    df = pd.read_csv(args.input_csv)
    Y_train = np.array(df.loc[:, "CPD":"OTH"])

    # read in npz file
    X_train = scipy.sparse.load_npz(args.input_npz)

    linearsvc_model = train_linearsvc(X_train, Y_train)

    with open(args.output_pk, 'wb') as handle:
        pickle.dump(linearsvc_model, handle, protocol=pickle.HIGHEST_PROTOCOL)
