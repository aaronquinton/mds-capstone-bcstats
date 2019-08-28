# -*- coding: utf-8 -*-
"""
emotion_analysis.py
Aaron Quinton, Ayla Pearson and Fan Nie
June 2019

This package performs emotion analysis.

Usage
-----
This file can be imported as python module and all functions can be used:

    Example:
    `from src.analysis.emotion_analysis import *`

"""

import spacy                         # Version 2.1.3
from spacy.matcher import Matcher
nlp = spacy.load('en_core_web_sm')

import matplotlib.pyplot as plt               # Version 3.0.2
import pandas as pd                           # Version 0.23.4
from pandas.api.types import is_numeric_dtype 
import numpy as np                            # Version 1.16.2
import random                                 # Version 3.7


###############################################################################
# Pre-process the raw data                                                    #
###############################################################################

def get_theme_labels(data, legend):
    """
    Obtains the main theme numbers

    Parameters
    ----------
    data: dataframe
        Dataframe that has the subtheme codes present in a column named 'code'
    legend: dataframe
        Legend that contains the subtheme codes and associated theme names and
        subtheme name

    Returns
    -------
    Returns a dataframe with a new column that has the main theme number
    and subtheme name

    """

    print("")
    # create copy so original is not overwritten
    data = data.copy()

    if 'code' not in data.columns:
        raise TypeError("'code' column not present in this dataset")
    if 'code' not in legend.columns:
        raise TypeError("'code' column not present in the legend")
    # ensure column is an int
    data['code'] = data['code'].astype(int)
    # join the legend labels to the dataset
    data = pd.merge(data, legend, on="code", how="left")
    data = data.drop(["theme_num"], axis=1)
    return data



def tidy_raw_comments(data):
    """
    Takes in the full comment data and gathers the codes into a single column
    while duplicating the text. This allows comparisons at the theme and
    sub-theme levels.

    Parameters
    ----------
    data: dataframe
        Input the raw survey comment data

    Returns
    -------
    Returns a dataframe with the codes gathered into a single column. Comments
    with multiple codes will be repeated.

    """

    data = data.copy()

    # replace all blank spaces with NaN values
    columns = ["code1", "code2", "code3", "code4", "code5"]
    for i in columns:
        if  is_numeric_dtype(data[i]) == False:
            condition = (data[i] != ' ')
            data[i] = data[i].where(condition, np.nan)

    # gather all subtheme codes to a single column
    data = pd.melt(data,
                    id_vars=["USERID", "text"],
                    value_vars=["code1", "code2", "code3", "code4", "code5"],
                    value_name="code").dropna()[['USERID', "code", "text"]]
    data['code'] = data['code'].astype(int)
    return data



def pre_process_comments(data, legend):
    """
    Tidy's the raw survey comments and add the theme and sub-theme names
    to the data set

    Parameters
    ----------
    data: dataframe
        Input the raw survey comment data
    legend: dataframe
        Legend that contains the subtheme codes and associated theme names and
        subtheme name

    Returns
    -------
    Returns a dataframe with the codes gathered into a single column. Comments
    with multiple codes will be repeated.

    """
    # create copy so original is not overwritten
    data = data.copy()
    # process the raw comments
    data = tidy_raw_comments(data)
    data = get_theme_labels(data, legend)
    return data


###############################################################################
#  Create Matchers and Find Emotion Scores for each Comment                   #
###############################################################################


def create_emotion_matcher(emotion_lexicon):
    """
    Adds all the rules for the emotion from a lexicon to the SpaCy Matcher.
    The rule adds the words to the matcher all in lower case.

    Parameters
    -----------
    emotion_lexicon: dataframe
        Dataframe that has the words to be added to rules of the matcher
        in a column named 'term'

    Returns
    -------
    Matcher: Spacy Object
        SpaCy matcher with all the words from the emotion lexicon added

    """
    matcher = Matcher(nlp.vocab)
    for word in emotion_lexicon['term']:
        dict_rule = {"LOWER" : word}
        matcher.add(word, None, [dict_rule])

    if not len(matcher) == emotion_lexicon.shape[0]:
        raise TypeError("Not all words were added to matcher")

    return matcher



def emotion_strength(text, matcher, emotion_lexicon):
    """
    Gets the strength of the emotion for each comment. Strength is calculated
    by summing the scores for each word.

    Parameters
    -------
    text: SpaCy tokens
        Give it the text to calculate emotion. This can be a word, sentence,
        comment or document level. All words must be lower case or they
        won't match with the matcher rules properly.
    matcher: SpaCy Matcher
        Matcher with the rules already created
    emotion_lexicon: dataframe
        Name of the emotion lexicon to relate the rule to the
        strength of the emotion (anger, fear, sad, joy). Must have
        the words under 'term' column and scores under 'score' column.

    Returns
    --------
    emotion_strength: sum
        Generates the strength of the emotion for the text

    """
    emotion_strength = []
    for i in range(len(text)):
        phrase_matches = matcher(text[i])
        # only parse through the non-zero lists
        if len(phrase_matches) != 0:
            count = 0
            # get the words from matched phrase
            for match_id, start, end in phrase_matches:
                words = []
                span = text[i][start:end]

                if not str(span).islower() == True:
                    raise TypeError("Text is not lowercase")

                words.append(span.text)
                # sum of strength of words by cross referencing emotion lexicon
                for j in words:
                    value = emotion_lexicon[emotion_lexicon["term"] == j]['score'].tolist()[0]
                    count = value + count
            emotion_strength.append(count)
        else:
            emotion_strength.append(0)
    return emotion_strength



def obtain_emotion_scores(data, lexicon, anger=True, fear=True, sadness=True,
                          joy=False):
    """
    Reads in the comments and lexicon and creates the rule matcher scores
    for each emotion for the comment. Warning this code can take over 15
    minutes to run due to the SpaCy tokenizer

    Parameters
    ----------
    data:
        Dataframe that contains the comments
        The column name needs to be: 'text' - comments
    lexicon:
        Dataframe that has the words and scores.
        The column names need to be:  'term' - words
                                      'score' - score
    anger: bool
        If you want this emotion included, the default is true
    fear : bool
        If you want this emotion included, the default is true
    sadness: bool
        If you want this emotion included, the default is true
    joy : bool
        If you want this emotion included, the default is false

    Returns
    --------
    Dataframe with the subtheme, text and sum of each emotion

    """
    # create a copy as to not write over original
    data = data.copy()
    # convert text to lower case
    data["text"] = data["text"].str.lower()
    # create SpaCy tokens
    comments = data["text"]
    docs = [nlp(comment) for comment in comments]
    # create specified emotion matchers
    if anger==True:
        anger = lexicon[lexicon["AffectDimension"]=="anger"]
        match_anger = create_emotion_matcher(anger)
        data["anger"] = emotion_strength(docs, match_anger, anger)
    if fear == True:
        fear = lexicon[lexicon["AffectDimension"]=="fear"]
        match_fear = create_emotion_matcher(fear)
        data["fear"] = emotion_strength(docs, match_fear, fear)
    if sadness == True:
        sad = lexicon[lexicon["AffectDimension"]=="sadness"]
        match_sad = create_emotion_matcher(sad)
        data["sad"] = emotion_strength(docs, match_sad, sad)
    if joy == True:
        joy = lexicon[lexicon["AffectDimension"]=="joy"]
        match_joy = create_emotion_matcher(joy)
        data["joy"] = emotion_strength(docs, match_joy, joy)

    return data




###############################################################################
# Filter and Clean Emotion Scores                                             #
###############################################################################



def list_emotion_present_in_data(data):
    """
    Inputs the data frame and generates a list of which emotions
    are present

    Parameters:
    -----------
    data: dataframe
        Dataframe with any of the columns anger, joy, fear and sad

    Returns
    -------
    Returns a list of the emotions names present

    """

    emotions_present = []
    if "anger" in data.columns:
        emotions_present.append("anger")
    if "fear" in data.columns:
        emotions_present.append("fear")
    if "sad" in data.columns:
        emotions_present.append("sad")
    if "joy" in data.columns:
        emotions_present.append("joy")
    return emotions_present



def one_hot_emotions(data, groupby=None, agreement=None):
    """
    Removes all the emotionless comments, labels the emotion of the comment
    based on the maximum emotion score and then converts the data to be one-hot
    encoding for the labels. It groups by the code and differences to ready
    the data for plotting.

    Parameters
    ----------
    data: dataframe
        Dataframe with columns USERID, code, diff, and the sum of the
        emotion scores for each comment
    groupby: str
        Variable the data needs to be grouped by, works for theme and
        subtheme levels
    agreement: bool
        Default is False which indicates you are working on original comments.
        When set to True it can be filtered for agreement differences
    Returns
    -------
    Cleaned dataframe that has emotion counts per subtheme and agreement level

    """
    # create a copy as to not write over original
    data = data.copy()
    # remove the emotionless comments
    data = filter_emotionless_comments(data)
    # obtains the max emotions for each comment and adds them to a new column
    emotion_list = list_emotion_present_in_data(data)
    data['encode'] = data[emotion_list].idxmax(1).tolist()

    if groupby == None:
        data = data.drop_duplicates(subset=['USERID'])
        df_reduced = data[['USERID']]
        df_one_hot = pd.concat([df_reduced, pd.get_dummies(data['encode'])],
                                                                axis=1)
        df_one_hot = df_one_hot[emotion_list].sum()
        return df_one_hot

    if agreement == False:
        # select columns from original data and add to one-hot encoding
        # of emotions
        df_reduced = data[['USERID', groupby]]
        df_one_hot = pd.concat([df_reduced, pd.get_dummies(data['encode'])],
                                                                    axis=1)
        # obtains counts for each sub theme and agreement level
        df_one_hot = df_one_hot.groupby([groupby], as_index=False).sum()
        return df_one_hot
    if agreement == True:
        # select columns from original data and add to 1 hot encoding
        # of emotions
        df_reduced = data[['USERID', groupby, 'diff']]
        df_one_hot = pd.concat([df_reduced, pd.get_dummies(data['encode'])],
                                                                axis=1)
        # obtains counts for each sub theme and agreement level
        df_one_hot = df_one_hot.groupby([groupby, 'diff'], as_index=False).sum()
        return df_one_hot


def filter_emotionless_comments(data):
    """
    Filters out comments where all the emotions have 0.0 for the
    summed scored. So this removes all the "emotionless" comments.

    Parameters
    ----------
    data: Dataframe with the sum of each emotion

    Returns
    -------
    Dataframe where all the "emotionless" comments have been filtered out

    """
    # create a copy as to not write over original
    data = data.copy()
    width = data.shape[1]
    # determine starting location of emotion scores
    count = 0
    for word in data.columns:
        if word == "anger":
            count += 1
        if word == "fear":
            count += 1
        if word == "sad":
            count += 1
        if word == "joy":
            count += 1

    start_loc = width - count
    # parse out only emotion score columns
    scores = data.iloc[:, start_loc:width]
    # get row wise sum, look for sums of zero
    # which indicates "emotionless" comments
    scores["sums"] = scores.sum(axis=1)
    data = data.copy()
    data["sums"] = scores.loc[:, "sums"]
    # remove comments where all the
    # emotions are zero
    data = data[data["sums"] != 0]
    data = data.drop("sums", axis=1)

    return data


def filter_depth(name, col_name, agreement, data):
    """
    Filters the dataframe to the theme or sub-theme level and agreement level
    if specified

    Parameters
    ----------
    name: str or integer
        Either input the name of the main theme or the number relating to
        the subtheme
    col_name: str
        Name of the column where the subtheme numbers or theme names are located
    agreement: str or int
        Either the agreement number of 0, 1, 2 or "all"
    data: dataframe
        Data with one-hot encoding with the counts of themes or subthemes
        by agreement level

    Returns
    -------
    Dataframe with the counts of each emotion filtered to the subtheme

    """
    # create a copy as to not write over original
    data = data.copy()
    if type(agreement) == int:
        if agreement not in [0, 1, 2]:
            raise TypeError("Agreement out of range")
            # filter to the sub-theme/theme and agreement level
        df_plot = data[(data[col_name] == name) & (data['diff'] == agreement)]
        return df_plot
    if agreement == "all":
            df_plot = data[(data[col_name] == name)]
            return df_plot
    if agreement == None:
        df_plot = data[(data[col_name] == name)]
        return df_plot


###############################################################################
# Plot Emotion Data                                                           #
###############################################################################

def create_bar_plot_percent(data):
    """
    Generates bar plot for data, adds emotionless comments to plot.

    Parameters
    ----------
    data: dataframe
        Counts are grouped by subtheme and agreement level for each emotion.
        Dataframe must be in long form where there is a column for each emotion.
    Returns
    -------
    fig:
        Returns matplotlib plot

    """
    # create a copy as to not write over original
    data = data.copy()
    # remove duplication due to multi-label comments
    data = data.drop_duplicates('USERID')
    # total number of comments
    full_data_size = data.shape[0]
    # filter out emotionless comments
    emotionless_removed_df = filter_emotionless_comments(data)
    emotionless_removed_size = emotionless_removed_df.shape[0]
    # obtain number of emotionless comments
    emotionless_size = full_data_size - emotionless_removed_size
    one_hot_df = one_hot_emotions(emotionless_removed_df,
                                    groupby=None,
                                    agreement=None)
    # add emotionless count to the emotion counts
    emotionless = pd.Series([emotionless_size], index=["emotionless"])
    one_hot_df = one_hot_df.append(emotionless)
    # obtain proportion of each emotion
    perc = one_hot_df/sum(one_hot_df)
    # plot proportion of each emotion
    perc = perc.rename({"sad":"sadness"})
    fig = plt.figure()
    ax = perc.plot.bar(rot=0, color=["#12AAB5",
                                     "#7C2F5B",
                                     "#2F5B7C",
                                     "lightgrey"])
    title = "Total Number of Comments " + str(full_data_size)
    plt.title(title)

    return fig




def plot_emotions(data, save_fig="reports/figures/emotion_plot.png",
                    depth=None, name=None, agreement=None):
    """
    Use this function to visualize the results of the emotion analysis. It will
    generate a bar plot showing the emotions and "emotionless" comments. The
    emotionless comments are comments that don't have the specified emotions
    present, there could be other emotions present that this analysis is not
    measuring and many not be truly emotionless.

    Parameters
    ----------
    data: dataframe
        Data containing the emotion scores for each comment. To visualize at the
        theme or sub-theme level the names must be present in the data set.
        To visualize at the agreement level the 'diff' column must be present,
        which contains the linkage scores.
    save_fig: str
        Default saves it in reports/figures. If None is given it will not save
        the figure.
    depth: str
        This parameters helps to filter the dataframe down to the theme or
        sub-theme level. Pass it the column name of where the themes names
        (ex: "theme") or sub-theme codes (ex: "codes") are present.
        The default is None which will give counts for all comments.
        To use name or agreement this cannot be set to None.
    name: str or integer
        Either input the name of the main theme (ex: "Executive",
        "Staffing Practices") or the number relating to the subtheme
        (ex: 12, 43, 102). Depth parameter must be specific as well as the name
        parameter. The default is None which gives counts for all comments.
    agreement: str
        Either input "all" to see all three levels together or input the
        level of agreement "strong", "weak", "no". Default is set to None
        which is for comments that have not be related to the multiple choice
        questions

    Returns
    -------
    figure
        Prints a plot to screen and saves the png

    Examples
    --------
    # the most common emotion in all the comments
    plot_emotions(df)
    # look at the emotion present in sub-theme - Reduce more political influence
    plot_emotions(df, depth="code", name=116)
    # look at the emotion present in theme - Supervisors
    plot_emotions(df, depth="theme", name="Supervisors")
    # look at emotions present in sub-theme - Increase Salary
    # with strong agreement
    plot_emotions(df, depth="code", name=24, agreement="strong" )
    """
    # create a copy as to not write over original
    data = data.copy()
    possible_agreements = ["strong", "weak", "no", None]
    if agreement not in possible_agreements:
        raise TypeError("Entered wrong agreement level")
    # create plot for all comments
    if depth == None:
        fig = create_bar_plot_percent(data)
    # filter to a theme, sub-theme or sub-theme and agreement_level
    else:
        # confirm parameters are entered correctly
        if depth not in data.columns:
            raise TypeError("column not present in dataset, double check" +
            "your column names")
        if name not in data[depth].unique():
            raise TypeError("theme/sub-theme not present in data")
        # match agreement level with value
        if agreement != None:
            dict_1 = {"strong" : 0,
                        "weak" : 1,
                        "no" : 2}
            agreement = dict_1[agreement]
        data = filter_depth(name, depth, agreement, data)
        fig = create_bar_plot_percent(data)
    # save or return the figures
    if save_fig == None:
        return fig
    else:
        return fig.savefig(save_fig, dpi=300)


###############################################################################
#  Explore Results                                                            #
###############################################################################


def normalize_scores(data):
    """
    Takes in the emotion scores and normalizes them by dividing by
    the total number of words per comment
    Parameter
    ---------
    data: dataframe
        Dataframe with the emotion scores
    Returns
    -------
    Dataframe normalized emotion scores

    """
    # create a copy as to not write over original
    data = data.copy()
    data["word_counts"] = data["text"].str.split().apply(len)
    # regularize scores to remove effect the comment length
    if "anger" in data.columns:
        data["anger"] = (data["anger"]/data["word_counts"])*100
    if "fear" in data.columns:
        data["fear"] = (data["fear"]/data["word_counts"])*100
    if "sad" in data.columns:
        data["sad"] = (data["sad"]/data["word_counts"])*100
    if "joy" in data.columns:
        data["joy"] = (data["joy"]/data["word_counts"])*100
    data = data.drop("word_counts", axis=1)
    data = data.round(3)
    return data


def display_top_emotions(data, emotion, n, order=False, normalize=False):
    """
    Display's either the highest or lowest emotion scores for the selected
    emotion. It first normalizes the scores to remove the effect of the comment
    length.

    Parameters
    ----------
    data: dataframe
        Dataframe with the emotion scores
    emotion: str
        The emotion to show the top or bottom scores either "anger", "fear",
        "sad", or "joy"
    n: int
        The number of comments to display
    order: bool
        Whether to show the top or bottom comments. The highest scores are
        shown by False which is the default.
    normalize: bool
        Can choose whether to divide the scores by the number of words. The
        default is to False which means they are not normalized, to
        normalize change to True.

    Returns
    -------
    The dataframe sorted to the chosen emotion in either ascending or
    descending order

    """
    # create a copy as to not write over original
    data = data.copy()
    if normalize == True:
        data = normalize_scores(data)
    # sort values
    data = data.sort_values(by=emotion, ascending=order)
    # remove user ID for printing
    data = data.drop("USERID", axis=1)
    # return selected number
    return data.head(n)

def examine_emotion_scoring(data, emotion, lexicon, index=None,
                                normalize=False):
    """
    Examine one comment in more detail by seeing the full comment and emotion
    scores. The one hot encoding under the columns "_emotion" show which
    emotion the comment is considered by a 1 in the column, a zero indicated it
    wasn't added to the count. A comment can only be coded to 1 emotion and is
    determined by the maximum score between the emotions.

    It also shows which emotion words were present in the comment and their
    associated score. The sum of the words should add to the values present
    in the table.

    The results are sorted into which emotion the comment was coded to, which
    is chosen with the emotion parameter. If no index is present then the
    function will randomly pick an example to show within the emotion.

    Parameters
    ----------
    data: dataframe
        Dataframe with the userid, subtheme, level of agreement, comments and
        total emotion score
    emotion: str
        Filters to comments related to the emotion of "anger", "fear",
        "joy", or "sad"
    lexicon: dataframe
        Emotion lexicon with words and score values
    normalize: bool
        Normalizes the scores so that comment length has been dealt with.
        The default is False, so the scores are not normalized, change to True
        to normalize the scores.

    Returns
    -------
    Displays the sum of the comment emotions scores, the max score, specific
    emotion words and their score.

    """
    # create a copy as to not write over original
    df = data.copy()
    if emotion not in data.columns:
        raise TypeError("emotion not present in dataframe")
    # get the max emotion and one hot-encoding
    df = filter_emotionless_comments(df)
    if normalize == True:
        df = normalize_scores(df)
    emotion_list = list_emotion_present_in_data(data)
    df['encode'] = df[emotion_list].idxmax(1).tolist()
    df_one_hot = pd.concat([df, pd.get_dummies(df['encode'], prefix="")],
                            axis=1)
    df_one_hot = df_one_hot.drop(["encode", "USERID"], axis=1)

    # create dataframes for filter condition
    if emotion == "anger":
        df1 = df_one_hot[df_one_hot['_anger'] == 1]
        row = random.randint(1, df1.shape[0])
    if emotion == "fear":
        df1 = df_one_hot[df_one_hot['_fear'] == 1]
        row = random.randint(1, df1.shape[0])
    if emotion == "joy":
        df1 = df_one_hot[df_one_hot['_joy'] == 1]
        row = random.randint(1, df1.shape[0])
    if emotion == "sad":
        df1 = df_one_hot[df_one_hot['_sad'] == 1]
        row = random.randint(1, df1.shape[0])
    # print row of dataframe
    if type(index) == int:
        if index not in df1.index.values.tolist():
            raise TypeError("the index value is not present in the" +
            "chosen emotion")
    if type(index) == int:
        # index to specific row index
        series = df1.loc[index]
        # convert back to dataframe for nice printing
        df1_display = pd.DataFrame(data = series.values.reshape(1,
                                                        series.shape[0]),
                                                        columns = series.index)
        df1_display = df1_display.set_index(pd.Index([index]))
        df1_display = df1_display.drop("text", axis=1)
        display(df1_display)
    elif index == None:
        df1_display = df1.drop("text", axis=1)
        display(df1_display.iloc[[row]])
    print("\n")
    print("Comment")
    print("-------")
    if type(index) == int:
        print(df1.loc[index]["text"])
        single_comment = nlp(df1.loc[index]["text"])
    elif index == None:
        print(df1['text'].tolist()[row])
        single_comment = nlp(df1['text'].tolist()[row])

    print("\n")
    # prints related words for each emotion
    if "anger" in emotion_list:
        anger = lexicon[lexicon['AffectDimension']=='anger']
        matches_anger = create_emotion_matcher(anger)(single_comment)
        print("ANGER")
        print_word_score(anger, matches_anger, single_comment)
    if "fear" in emotion_list:
        fear = lexicon[lexicon['AffectDimension']=='fear']
        matches_fear = create_emotion_matcher(fear)(single_comment)
        print("FEAR")
        print_word_score(fear, matches_fear, single_comment)
    if "joy" in emotion_list:
        joy = lexicon[lexicon['AffectDimension']=='joy']
        matches_joy = create_emotion_matcher(joy)(single_comment)
        print("JOY")
        print_word_score(joy, matches_joy, single_comment)
    if "sad" in emotion_list:
        sad = lexicon[lexicon['AffectDimension']=='sadness']
        matches_sad = create_emotion_matcher(sad)(single_comment)
        print("SAD")
        print_word_score(sad, matches_sad, single_comment)


def print_word_score(lexicon, matcher, comment):
    """
    Prints the word and its score for the given comment

    Parameters
    ----------
    lexicon: dataframe
        Dataframe that contains the emotion words and their scores. The
        words need to be in a column named "term" and the scores in a
        column named "score"
    matcher: SpaCy Matcher
        Matcher with the rules already created
    comment: str
        The comment to have the specific words parsed from

    Returns
    -------
    Prints the words and their related score for the given comment

    """
    print("-----")
    for match_id, start, end in matcher:
        words = []
        span = str(comment[start:end])
        value = lexicon[lexicon["term"] == span]['score'].tolist()[0]
        print("{0} {1:.3f}".format(span, value))
    print("\n")



def summary(data):
    """
    Displays a summary table showing the total number of rows, unique comments,
    emotionless comments, comments with any of the one emotions and comments
    where the emotion had the highest score.

    Parameters
    ----------
    data: dataframe
        Dataframe with the emotions per comment

    Returns
    -------
    Returns a dataframe showing summary stats.

    """
    col1_names = []
    col2_values = []
    # count number of rows
    total_rows = data.shape[0]
    col1_names.append("Rows")
    col2_values.append(total_rows)
    # number of unique comments
    total_comments = data.drop_duplicates(subset=['USERID']).shape[0]
    col1_names.append("Unique Comments")
    col2_values.append(total_comments)
    # number of emotionless comments
    emotionless_removed = filter_emotionless_comments(data).shape[0]
    emotionless_commnets = total_rows - emotionless_removed
    col1_names.append("Emotionless Comments")
    col2_values.append(emotionless_commnets)
    # counts of comments per emotion
    emotion_list = list_emotion_present_in_data(data)
    one_hot_df = one_hot_emotions(data, groupby=None, agreement=None)
    # count of anger comments
    if "anger" in emotion_list:
        any_anger_comments = np.sum(data["anger"] != 0)
        col1_names.append("Comments with any Anger")
        col2_values.append(any_anger_comments)
        all_anger_comments = one_hot_df["anger"]
        col1_names.append("Comments with max Anger")
        col2_values.append(all_anger_comments)
    # count of fear comments
    if "fear" in emotion_list:
        any_fear_comments = np.sum(data["fear"] != 0)
        col1_names.append("Comments with any Fear")
        col2_values.append(any_fear_comments)
        all_fear_comments = one_hot_df["fear"]
        col1_names.append("Comments with max Fear")
        col2_values.append(all_fear_comments)
    # count of joy comments
    if "joy" in emotion_list:
        any_joy_comments = np.sum(data["joy"] != 0)
        col1_names.append("Comments with any Joy")
        col2_values.append(any_joy_comments)
        all_joy_comments = one_hot_df["joy"]
        col1_names.append("Comments with max Joy")
        col2_values.append(all_joy_comments)
    # count of sad comments
    if "sad" in emotion_list:
        any_sad_comments = np.sum(data["sad"] != 0)
        col1_names.append("Comments with any Sadness")
        col2_values.append(any_sad_comments)
        all_sad_comments = one_hot_df["sad"]
        col1_names.append("Comments with max Sadness")
        col2_values.append(all_sad_comments)
    # create a dataframe to display the results
    d = {"Total Number of:":col1_names ,"Count":col2_values}
    return pd.DataFrame(data=d)
