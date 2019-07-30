#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

CS5010: Final Project
Names: Aditi Rajagopal, Bradley Katcher, Charlie Putnam
Computing-ID: ar5vt, bk5pu, cmp2cz
Content: /r/CFB web scraper looking at rivalry data
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
        #with open('creds.json') as config_file:
        #    data = json.load(config_file)

        reddit = praw.Reddit(client_id = "Jzm3pXTmnfuLug",
            client_secret = "uL8tiUV8UOVkhgJBa7pqSAcDgTM",
            username = "uva_dsi_test_dev",
            password = "smoothtomato330",
            user_agent = "test-app by /u/uva_dsi_test_dev")
        submission = reddit.submission(url=self.URL)

        # Iterate over all of the top-level comments on the post, get author, fliar, comment, timestamp
        # got the keys from looking json version of the website 
        # TO DO: figure out whether or not we are grabbing all the comments, or just the top-level ones (flatten tree?)
        for comment in submission.comments:
            try:
                #Clean comment bodies of hyperlinks, which can affect Vader Sentiments
                comment.body = re.sub(r'\(http\S+' ,'', comment.body)
            
                #remove brackets and parens
                comment.body  = re.sub('\[|\]|\(|\)|\?','', comment.body)
                
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
                    "votes": comment.score
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