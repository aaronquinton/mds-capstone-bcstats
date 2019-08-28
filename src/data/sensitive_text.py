# sensitive_text.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-05-16

# General USAGE:
# This script defines functions to identify comments that contain senstive
# information. To use you need to have the NationalNames.csv on your local
# computer and saved in the project directory:
# "./references/data-dictionaries/NationalNames.csv"
# The csv can be downloaded on kaggle at the following link:
# https://www.kaggle.com/kaggle/us-baby-names#NationalNames.csv

# For Makefile, you only need to decide to use one or the other below:

# USAGE:
'''
python src/data/sensitive_text.py \
--input_xlsx data/raw/2018\ WES\ Qual\ Coded\ -\ Final\ Comments\ and\ Codes.xlsx \
--output_csv data/interim/desensitized_qualitative-data2018.csv \
--skiprows 1
'''

# USAGE for Sample Data:
'''
python src/data/sensitive_text.py \
--input_xlsx data/raw/2018_wes_qual_sample.xlsx \
--output_csv data/interim/desensitized_qualitative-data2018.csv \
--skiprows 0
'''


# Import Modules
import pandas as pd
import spacy
import argparse
import numpy as np

# Default File paths:
filepath_in = "data/raw/2018 WES Qual Coded - Final Comments and Codes.xlsx"
filepath_out = "data/interim/desensitized_qualitative-data2018.csv"


def get_arguments():
    parser = argparse.ArgumentParser(description='Remove sensitive comments'
                                     'from excel WES survey and write to csv')

    parser.add_argument('--input_xlsx', '-i', type=str, dest='input_xlsx',
                        action='store', default=filepath_in,
                        help='the input xlsx file')

    parser.add_argument('--output_csv', '-o', type=str, dest='output_csv',
                        action='store', default=filepath_out,
                        help='the output csv file')

    parser.add_argument('--skiprows', '-s', type=int, dest='skiprows',
                        action='store', default='1',
                        help='Number of rows to skip when reading xlsx')

    args = parser.parse_args()
    return args


###############################################################################
# Create name_check list based on US Census data to be used in the            #
# sensitive_text function                                                     #
###############################################################################

# File Paths to read in datadictionary
filepath_names = "./references/data-dictionaries/NationalNames.csv"

# Read in data dictionary
df_names = pd.read_csv(filepath_names)
name_check = df_names.Name.unique().tolist()

# Names that are in the names list and NER labels as Person, but are not
# actually sensitive. ie. they are false positives
false_names = ['Sheriff', 'Law', 'Child', 'Warden', 'Care', 'Cloud', 'Honesty',
               'Maple', 'Marijuana', 'Parks', 'Ranger', 'Travel', 'Young',
               'Branch', 'Field', 'Langford', 'Surrey', 'Cap', 'Lean', 'Van',
               'Case', 'Min', 'Merit', 'Job', 'Win', 'Forest', 'Victoria']

# Drop the false_names from the names list
name_check = list(set(name_check).difference(set(false_names)))

# Names that are not in the names list, but should be! ie. false negatives
missing_names = ['Kristofferson']

# Add missing names
for missing_name in missing_names:
    name_check.append(missing_name)


###############################################################################
# Define functions and set up script to run in command line                   #
###############################################################################
def find_sensitive_text(comments):
    """Return a list of indices identifying comments with sensitive information
    given a list of comments"""

    # Apply Named entity recognition on list of comments
    nlp = spacy.load("en_core_web_sm")
    docs = [nlp(str(comment)) for comment in comments]

    # Create a list of the words tagged as PERSON and the original index
    person_index = []
    person_list = []
    for index, doc in enumerate(docs):
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                person_index.append(index)
                person_list.append(ent.text)

    # Cross check a name dictionary to confirm names
    sensitive_person = []
    sensitive_person_index = []
    for index, person in enumerate(person_list):
        for name in person.split():
            if name in name_check:
                sensitive_person.append(person)
                sensitive_person_index.append(person_index[index])
                break

    return sensitive_person_index


def remove_sensitive_text(filepath, skiprows):

    df = pd.read_excel(filepath, skiprows=skiprows)
    df = df[df.iloc[:, 1].isnull() == False]
    comments = df.iloc[:, 1]
    sensitive_indices = find_sensitive_text(comments)
    df = df.drop(index=sensitive_indices)

    return(df)


###############################################################################
if __name__ == "__main__":

    args = get_arguments()
    df = remove_sensitive_text(args.input_xlsx, args.skiprows)
    df.to_csv(args.output_csv, index=False)
