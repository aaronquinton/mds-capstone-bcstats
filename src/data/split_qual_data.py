# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: May 2019
# This script file is for splitting the comment datasets into a train and test
# to ensure dataset test data is untouched during our analysis

# USAGE:
'''
python src/data/split_qual_data.py \
--input_csv data/interim/desensitized_qualitative-data2018.csv \
--output_csv1 data/interim/test_2018-qualitative-data.csv \
--output_csv2 data/interim/train_2018-qualitative-data.csv
'''

import pandas as pd
import argparse

# Default File paths:
filepath_in = "data/interim/desensitized_qualitative-data2018.csv"
filepath_out_test = "data/interim/test_2018-qualitative-data.csv"
filepath_out_train = "data/interim/train_2018-qualitative-data.csv"


def get_arguments():
    parser = argparse.ArgumentParser(description='Remove sensitive comments'
                                     'from excel WES survey and write to csv')

    parser.add_argument('--input_csv', '-i', type=str, dest='input_csv',
                        action='store', default=filepath_in,
                        help='the input csv file')

    parser.add_argument('--output_csv1', '-o', type=str, dest='output_csv1',
                        action='store', default=filepath_out_test,
                        help='the test output csv file')

    parser.add_argument('--output_csv2', '-o2', type=str, dest='output_csv2',
                        action='store', default=filepath_out_train,
                        help='the train output csv file')

    args = parser.parse_args()
    return args


###############################################################################
if __name__ == "__main__":

    args = get_arguments()

    df_raw_2018 = pd.read_csv(args.input_csv)

    df_test_2018 = df_raw_2018.sample(frac=0.1, random_state=2019)
    df_train_2018 = df_raw_2018.drop(index=df_test_2018.index)

    df_test_2018.to_csv(path_or_buf=args.output_csv1, index=False)
    df_train_2018.to_csv(path_or_buf=args.output_csv2, index=False)
