
# example_predict.py
# Author: Fan Nie, Ayla Pearson, Aaron Quinton
# Date: 2019-06-26

# Use script for quick demo to type an example comment at the command line.
# The script utilizes the models for predictions

text = input("Type Comment: ")


import sys
sys.path.insert(1, '.')
import warnings
warnings.filterwarnings("ignore")
import pickle
import pandas as pd
from src.features.encode_comments import get_encoded_comments
import numpy as np
from keras.models import load_model


df = pd.DataFrame({'comment': [text]})
comments = df.iloc[:, 0]

embed_names = ['glove_crawl', 'glove_wiki', 'fasttext_crawl']

# Load Embedding Tokenizers
with open('./models/embed_tokenizers.pickle', 'rb') as handle:
    embed_tokenizers = pickle.load(handle)

# Load Neural Net Classification Models
conv1d = load_model('./models/conv1d_models.h5')

# Make predictions
encoded_comments = {}
for embed in embed_names:
    encoded_comments[embed] = get_encoded_comments(comments,
                                                   embed_tokenizers[embed],
                                                   embed)

Y_pred = conv1d.predict(encoded_comments['glove_wiki'])

# Format predictions and save to csv
predictions = pd.DataFrame(np.round(Y_pred))

predictions['comment'] = comments
predictions.columns = ['CPD', 'CB', 'EWC', 'Exec', 'FWE', 'SP', 'RE', 'Sup',
                       'SW', 'TEPE', 'VMG', 'OTH', 'comment']

df = predictions[['comment', 'CPD', 'CB', 'EWC', 'Exec', 'FWE',
                  'SP', 'RE', 'Sup', 'SW', 'TEPE', 'VMG', 'OTH']]

print(df)
