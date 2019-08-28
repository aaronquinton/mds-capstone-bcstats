# preprocessing_text.py
# Authors: Aaron Quinton
# Date: 2019-05-22

# Many functions and the overall workflow have been built from a Kaggle Kernel
# written by "Dieter"
# https://www.kaggle.com/christofhenkel/how-to-preprocessing-when-using-embeddings

# Import modules
import re
import operator
import numpy as np
from tqdm import tqdm
tqdm.pandas()


###############################################################################
# Functions used for preprocessing punctuation, numbers, and misspellings     #
###############################################################################
def clean_text(x):
    '''Replace punctuations in a string with spaces or nothing.
    Useful for pretrained embeddings.

    Parameters
    ----------
    x : str

    Returns
    -------
    x : a string with cleaned punctuations
    '''
    x = str(x)
    for punct in "/-'":
        x = x.replace(punct, ' ')
    for punct in '&':
        x = x.replace(punct, f' {punct} ')
    for punct in '?!.,"#$%\'()*+-/:;<=>@[\\]^_`{|}~' + '“”’':
        x = x.replace(punct, '')

    return x


def clean_numbers(x):
    '''Replaces numbers greater than 9 with # for each digit.
    Ex. 150 becomes ###. This is useful for pretrained embeddings.

    Parameters
    ----------
    x : str

    Returns
    -------
    x : a string with clean numbers
    '''
    x = re.sub('[0-9]{5,}', '#####', x)
    x = re.sub('[0-9]{4}', '####', x)
    x = re.sub('[0-9]{3}', '###', x)
    x = re.sub('[0-9]{2}', '##', x)
    return x


def _get_mispell(mispell_dict):
    mispell_re = re.compile('(%s)' % '|'.join(mispell_dict.keys()))
    return mispell_dict, mispell_re


mispell_dict = {'colour': 'color',
                'centre': 'center',
                'didnt': 'did not',
                'doesnt': 'does not',
                'isnt': 'is not',
                'shouldnt': 'should not',
                'behaviour': 'behavior',
                'behaviours': 'behaviors',
                'behavioural': 'behavioral',
                'favourite': 'favorite',
                'favouritism': 'favoritism',
                'travelling': 'traveling',
                'counselling': 'counseling',
                'theatre': 'theater',
                'acknowledgement': 'acknowledgment',
                'cancelled': 'canceled',
                'labour': 'labor',
                'organisation': 'organization',
                'wwii': 'world war 2',
                'citicise': 'criticize',
                'counsellor': 'counselor',
                'favour': 'favor',
                'defence': 'defense',
                'practise': 'practice',
                'instagram': 'social medium',
                'whatsapp': 'social medium',
                'snapchat': 'social medium'
                }
mispellings, mispellings_re = _get_mispell(mispell_dict)


def replace_typical_misspell(text):
    '''Replace common misspellings in a string with correct spelling.
    Useful for pretrained embeddings.

    Parameters
    ----------
    x : str

    Returns
    -------
    x : a string with corrected spelling
    '''
    def replace(match):
        return mispellings[match.group(0)]

    return mispellings_re.sub(replace, text)


def remove_stopwords(sentences):
    '''Removes common stopwords from a tokenized list of words

    Parameters
    ----------
    x : list of words

    Returns
    -------
    x : list of words with stop words removed
    '''
    to_remove = ['a', 'to', 'of', 'and']

    sentences_re = [[word for word in sentence if word not in to_remove]
                    for sentence in sentences]

    return sentences_re


def preprocess_for_embed(text, embeddings_index, split=True):
    '''Preprocess text data from a dataframe based on the pretrained embedding

    Parameters
    ----------
    text : Pandas series object
    embeddings_index: The name of the pretrained embedding

    Returns
    -------
    text : list of tokenized words for each comment
    '''
    if embeddings_index in ['glove_wiki', 'glove_twitter', 'w2v_base_model']:
        text = text.apply(lambda x: clean_text(x)) \
                   .apply(lambda x: replace_typical_misspell(x)) \
                   .apply(lambda x: clean_numbers(x)) \
                   .apply(lambda x: x.lower())

        if split:
            text = remove_stopwords(text.str.split())
        return text

    if embeddings_index == 'w2v_google_news':
        text = text.apply(lambda x: clean_text(x)) \
                   .apply(lambda x: replace_typical_misspell(x)) \
                   .apply(lambda x: clean_numbers(x))

        if split:
            text = remove_stopwords(text.str.split())
        return text

    else:
        text = text.apply(lambda x: clean_text(x)) \
                   .apply(lambda x: replace_typical_misspell(x))

        if split:
            text = remove_stopwords(text.str.split())
        return text


def preprocess_for_bow(text):
    '''Preprocess text data for the bag of words model

    Parameters
    ----------
    text : Pandas series object

    Returns
    -------
    text : numpy array
    '''
    text = text.apply(lambda x: clean_text(x)) \
               .apply(lambda x: replace_typical_misspell(x)) \
               .apply(lambda x: x.lower())

    return np.array(text)


def balance_themes(X, Y):
    '''Balances arrays to have roughly the same number of comments for each
    class

    Parameters
    ----------
    X : numpy array with comment text

    Returns
    -------
    Y : numpy array with comment labels
    '''
    counts = np.sum(Y, axis=0)

    for i in range(Y.shape[1]):

        X_labeled = X[Y[:, i] == 1, :]
        Y_labeled = Y[Y[:, i] == 1, :]

        index = np.random.randint(low=0, high=counts[i],
                                  size=max(counts) - counts[i])
        X_array_to_append = X_labeled[index, :]
        Y_array_to_append = Y_labeled[index, :]

        if i == 0:
            X_balance = X
            Y_balance = Y

        X_balance = np.vstack((X_balance, X_array_to_append))
        Y_balance = np.vstack((Y_balance, Y_array_to_append))

    return X_balance, Y_balance


def build_vocab(sentences, verbose=True):
    vocab = {}
    for sent in tqdm(sentences, disable=(not verbose)):
        for word in sent:
            try:
                vocab[word] += 1
            except KeyError:
                vocab[word] = 1
    return vocab


def check_coverage(vocab, embeddings_index):
    a = {}
    oov = {}
    k = 0
    i = 0
    for word in tqdm(vocab):
        try:
            a[word] = embeddings_index[word]
            k += vocab[word]
        except:
            oov[word] = vocab[word]
            i += vocab[word]
            pass

    vocab_coverage = len(a) / len(vocab)
    text_coverage = k / (k + i)
    sorted_x = sorted(oov.items(), key=operator.itemgetter(1))[::-1]

    return vocab_coverage, text_coverage, sorted_x
