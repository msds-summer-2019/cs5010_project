#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

CS5010: Final Project
Names: Aditi Rajagopal, Bradley Katcher, Charlie Putnam
Computing-ID: ar5vt, bk5pu, cmp2cz
Notes: /r/CFB web scraper looking at rivalry data
TO DO: clean up class, decide what to do with data....Scikit-Learn?
"""
import praw, datetime, json
import re
import nltk
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

class RedditPostParse: 

    def __init__(self, URL, flair1, flair2):
        self.URL = URL
        self.flair1 = flair1
        #self.flair1DF = []
        self.flair2 = flair2
        #self.flair2DF = []
        self.postDetails = []
        self.postDF = []

# =============================================================================
#     def clean_comments(comment_body):
#         
#         #remove hyperlinks:
#         comment_body = re.sub(r'\(http\S+' ,'', comment_body)
#     
#         #remove brackets and parens
#         comment_body = re.sub('\[|\]|\(|\)','', comment_body)
#         return comment_body
# =============================================================================
    
    def getComments(self):
        
        # create Reddit object by passing credentials to Praw, get creds from creds.json
        with open('creds.json') as config_file:
            data = json.load(config_file)

        reddit = praw.Reddit(client_id = data['client_id'],
            client_secret = data['client_secret'],
            username = data['user'],
            password = data['password'],
            user_agent = data['user_agent'])
        submission = reddit.submission(url=self.URL)

        # Iterate over all of the top-level comments on the post, get author, fliar, comment, timestamp
        # got the keys from looking json version of the website 
        # TO DO: figure out whether or not we are grabbing all the comments, or just the top-level ones (flatten tree?)
        for comment in submission.comments:
            try:
                #Clean comment bodies of hyperlinks, which can affect Vader Sentiments
                comment.body = re.sub(r'\(http\S+' ,'', comment.body)
            
                #remove brackets and parens
                comment.body  = re.sub('\[|\]|\(|\)','', comment.body)
                
                analyzer = SentimentIntensityAnalyzer()
                sentimentScore = analyzer.polarity_scores(comment.body)

                blob = TextBlob(comment.body)
                blobScore = []
                for sentence in blob.sentences:
                    blobScore.append(sentence.sentiment.polarity)

                self.postDetails.append({
                    "author" : comment.author,
                    "flair": comment.author_flair_text,
                    "comment": comment.body,
                    "timeStamp": datetime.datetime.fromtimestamp(comment.created_utc),
                    "sentimentScore": sentimentScore,
                    "textblobScore": blobScore,
                    "votes", comment.score
                })
            except:
                continue
          
    #cleans Flairs and creates a new column in the postDF with either flair 1, flair 2, or neither
    def clean_extractFlairValues(self):
        
        #convert flairs of None to empty string to make cleaner easier
        self.postDF['flair'] = self.postDF['flair'].apply(lambda x: '' if x is None else x)
        #remove any numbers from flairs e.g. ohiostate2 -> ohiostate
        self.postDF['flair'] = self.postDF['flair'].apply(lambda x: ''.join([d for d in x if not d.isdigit()]))
        
        #if/else conditions on flair, check that the two flairs are in flair field
        #semicolons necessary to exclude cases where 'michigan state' is a false positive for 'michigan'
        conditions = [
            self.postDF['flair'].str.contains(':' + self.flair1 + ':', na = False),
            self.postDF['flair'].str.contains(':' + self.flair2 + ':', na = False)]
        
        choices = [self.flair1, self.flair2]
        
        #Assign new column to postDF with extracted values
        self.postDF['flair_clean'] = np.select(conditions, choices, default='neither')
        
    #Creates 4 columns from sentimentScore field: neg, neu, pos, and compound
    def explode_sentimentScores(self):
        self.postDF[['neg','neu','pos','compound']] = self.postDF['sentimentScore'].apply(pd.Series)
        self.postDF.drop('sentimentScore', axis=1, inplace = True)

        
    def getDataFrame(self):
        # put everything into a dataframe
        self.postDF = pd.DataFrame(self.postDetails, columns=['author', 'flair', 'comment', 'timeStamp','sentimentScore','textblobScore','votes'])
        self.postDF['timeStamp'] = pd.to_datetime(self.postDF['timeStamp'])
        self.postDF = self.postDF.sort_values(by='timeStamp',ascending=True)
        
        #Create column 'flair_clean' that extracts if the commenter has flair 1 or flair 2, or neither
        self.clean_extractFlairValues()
        
        #Creates 4 columns, one for each key in sentimentScore dict
        self.explode_sentimentScores()
        
        return self.postDF

uofm_osu_firsthalf = RedditPostParse("https://www.reddit.com/r/CFB/comments/9zzk5n/game_thread_michigan_ohio_state_1200pm_et/", 'michigan', 'ohiostate')
uofm_osu_firsthalf.getComments()
uofm_osu_firsthalf_df = uofm_osu_firsthalf.getDataFrame()

uofm_osu_secondhalf = RedditPostParse("https://www.reddit.com/r/CFB/comments/a018xs/game_thread_michigan_ohio_state_1200pm_et_second/", 'michigan', 'ohiostate')
uofm_osu_secondhalf.getComments()
uofm_osu_secondhalf_df = uofm_osu_secondhalf.getDataFrame()


uofm_osu = pd.concat([uofm_osu_firsthalf_df, uofm_osu_secondhalf_df])

#Timestamp stuff
#uofm_osu.groupby(pd.Grouper(key='timeStamp', freq='5min'))

#convert sentiment scores to their own columns, to implement soon
# =============================================================================
uofm_osu[['neg','neu','pos','compound']] = uofm_osu['sentimentScore'].apply(pd.Series)
# 
# uofm_osu.head()
# 
# sentences= ['fuck ohio',
#             '[fuck ohio]',
#             '[fuck ohio] (https://i.imgur.com/hyIMZmw.jpg) text text fdsafds']
# 
# analyzer = SentimentIntensityAnalyzer()
# for sentence in sentences:
#     vs = analyzer.polarity_scores(sentence)
#     print("{:-<65} {}".format(sentence, str(vs)))
# 
# #remove hyperlinks:
#     re.sub(r'\(http\S+' ,'', sentences[2])
#     
# #remove brackets and parens
#     re.sub('\[|\]|\(|\)','',sentences[2])
# 
# =============================================================================

uofm_osu.to_csv('uofm_osu.csv') #exports results to a csv


uofm_msu_firsthalf = RedditPostParse("https://www.reddit.com/r/CFB/comments/9puso8/game_thread_michigan_michigan_state_1200pm_et/", 'michigan', 'michiganstate')
uofm_msu_firsthalf.getComments()
uofm_msu_firsthalf_df = uofm_msu_firsthalf.getDataFrame()

uofm_msu_secondhalf = RedditPostParse("https://www.reddit.com/r/CFB/comments/9pwu6h/game_thread_michigan_michigan_state_1200pm_et/", 'michigan', 'michiganstate')
uofm_msu_secondhalf.getComments()
uofm_msu_secondhalf_df = uofm_msu_secondhalf.getDataFrame()

uofm_msu = pd.concat([uofm_msu_firsthalf_df, uofm_msu_secondhalf_df])

uofm_msu.to_csv('uofm_msu.csv') #exports results to a csv

uofMComments = uofm_msu[uofm_msu['flair'].str.contains(":michigan:", na = False)]
msuComments = uofm_msu[uofm_msu['flair'].str.contains(":michiganstate:", na = False)]

uofm_msu_comments = uofm_msu.comment.values

# based on https://www.mikulskibartosz.name/word-cloud-from-a-pandas-data-frame/
wordcloud = WordCloud(
    width = 3000,
    height = 2000,
    background_color = 'black',
    stopwords = STOPWORDS).generate(str(uofm_msu_comments))
fig = plt.figure(
    figsize = (40, 30),
    facecolor = 'k',
    edgecolor = 'k')
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()

#uofMComments.head()
#msuComments.head()
