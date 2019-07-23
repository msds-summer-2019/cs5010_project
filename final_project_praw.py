#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

CS5010: Final Project
Names: Aditi Rajagopal, Bradley Katcher, Charlie Putnam
Computing-ID: ar5vt, bk5pu, cmp2cz
Notes: /r/CFB web scraper looking at rivalry data
TO DO: pull .json data from each post
"""

#praw package
import praw
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import creds
#separate file to store credentials for PRAW, file named creds.py


client_id = creds.client_id
client_secret = creds.client_secret
user = creds.user
password = creds.password
user_agent = creds.user_agent

class RedditPostParse: 

    def __init__(self, URL, flair1, flair2):
        self.URL = URL
        self.flair1 = flair1
        self.flair2 = flair2
        self.postDetails = []
        self.postDF = []

    def getComments(self):
        
        #create Reddit object by passing credentials to Praw
        reddit = praw.Reddit(client_id = 'Jzm3pXTmnfuLug',
            client_secret = 'uL8tiUV8UOVkhgJBa7pqSAcDgTM',
            username = 'uva_dsi_test_dev',
            password = 'smoothtomato330',
            user_agent = 'test-app by /u/uva_dsi_test_dev')
        #submission.load_more_comments(limit=None, threshold=1)
        submission = reddit.submission(url=self.URL)

        # Iterate over all of the top-level comments on the post:
        for comment in submission.comments:
            try:
                analyzer = SentimentIntensityAnalyzer()
                sentimentScore = analyzer.polarity_scores(comment.body)
                self.postDetails.append({
                    "author" : comment.author,
                    "flair": comment.author_flair_text,
                    "comment": comment.body,
                    "timeStamp": comment.created_utc,
                    "sentimentScore": sentimentScore,
                })
            except:
                continue

    #def sortFlairs(self):
        # Obtain all flairs, split into multiple columns if there are multiple flairs, condense into one list and make that a dataframe
    #    flair = self.postDF.flair.str.split(pat= " • " , n=-1, expand=True)
    #    flair1 = flair[0]   #initial flair
    #    flair2 = flair[1]   #secondary flair - displays as None if no flair exists
    #    flair1.str.strip()
    #    flair2.str.strip()
    #    flairTot = flair1.append(flair2, ignore_index = True) #create one column with all flairs and then import that into a dataframe for anlaysis
    #    flairTot = pd.DataFrame(data = flairTot, columns = ['flairs'])

        
    def getDataFrame(self):
        self.postDF = pd.DataFrame(self.postDetails, columns=['author', 'flair', 'comment', 'timeStamp','sentimentScore'])
        # self.postDF['timeStamp'] = pd.to_datetime(self.postDF['timeStamp'])
        # self.postDF['timeStamp'] = pd.to_datetime(self.postDF['timeStamp'], format="%Y%m%d:%H:%M:%S.%f").sort_values()
        return self.postDF

CFB = RedditPostParse("https://www.reddit.com/r/CFB/comments/9zzk5n/", 'michigan', 'osu')
CFB.getComments()
cfb = CFB.getDataFrame()
cfb.to_csv('CFB.csv') #exports results to a csv
