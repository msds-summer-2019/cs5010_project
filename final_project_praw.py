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
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class RedditPostParse: 

    def __init__(self, URL, flair1, flair2):
        self.URL = URL
        self.flair1 = flair1
        #self.flair1DF = []
        self.flair2 = flair2
        #self.flair2DF = []
        self.postDetails = []
        self.postDF = []

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
                analyzer = SentimentIntensityAnalyzer()
                sentimentScore = analyzer.polarity_scores(comment.body)
                self.postDetails.append({
                    "author" : comment.author,
                    "flair": comment.author_flair_text,
                    "comment": comment.body,
                    "timeStamp": datetime.datetime.fromtimestamp(comment.created_utc),
                    "sentimentScore": sentimentScore,
                })
            except:
                continue
        
    def getDataFrame(self):
        # put everything into a dataframe
        self.postDF = pd.DataFrame(self.postDetails, columns=['author', 'flair', 'comment', 'timeStamp','sentimentScore'])
        self.postDF['timeStamp'] = pd.to_datetime(self.postDF['timeStamp'])
        self.postDF = self.postDF.sort_values(by='timeStamp',ascending=True)
        
        # not sure how to handle the flairs atm. do we create the dataframe based on the flairs within the class?
#        self.flair1DF = self.postDF[self.postDF['flair'].str.contains(self.flair1, na = False)]
#        self.flair2DF = self.postDF[self.postDF['flair'].str.contains(self.flair2, na = False)]
        
        return self.postDF

uofm_osu_firsthalf = RedditPostParse("https://www.reddit.com/r/CFB/comments/9zzk5n/game_thread_michigan_ohio_state_1200pm_et/", 'michigan', 'ohiostate')
uofm_osu_firsthalf.getComments()
uofm_osu_firsthalf_df = uofm_osu_firsthalf.getDataFrame()

uofm_osu_secondhalf = RedditPostParse("https://www.reddit.com/r/CFB/comments/a018xs/game_thread_michigan_ohio_state_1200pm_et_second/", 'michigan', 'ohiostate')
uofm_osu_secondhalf.getComments()
uofm_osu_secondhalf_df = uofm_osu_secondhalf.getDataFrame()

uofm_osu = pd.concat([uofm_osu_firsthalf_df, uofm_osu_secondhalf_df])

uofm_osu.to_csv('uofm_osu.csv') #exports results to a csv

michiganComments = uofm_osu[uofm_osu['flair'].str.contains(":michigan:", na = False)]
osuComments = uofm_osu[uofm_osu['flair'].str.contains(":ohiostate:", na = False)]
michiganComments.head()
osuComments.head()


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
uofMComments.head()
msuComments.head()
