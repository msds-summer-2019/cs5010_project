# -*- coding: utf-8 -*-
"""
Homework 3: Python

Name: Charlie Putnam
Computing ID: cmp2cz
"""

#praw package
import praw
import pandas as pd
#separate file to store credentials for PRAW, file named creds.py
import creds

#set credentials
client_id = creds.client_id
client_secret = creds.client_secret
user = creds.user
password = creds.password
user_agent = creds.user_agent

#create Reddit object by passing credentials to Praw
reddit = praw.Reddit(client_id = client_id,
            client_secret = client_secret,
            username = user,
            password = password,
            user_agent = user_agent)

#Sub-reddit of interest
sub = 'NFL'


def redditCrawler(reddit, sub, post_limit = 100):
    """
    Returns a data frame of Submission Title, Score, Upvote Ratio, 
    Number of Comments, URL, and text when a user passes in a subreddit. 
    Automatically pulls data from the "Hot" category at that point in time.
    
    Args:
        reddit: reddit object created from praw package
        sub: string of subreddit, found in url after /r/
            i.e. r/'NFL' or r/'CFB'
        post_limit: number of posts to extract (default = 100)
    
    Returns:
        Dictionary with each key being the submissions ID, and every sub-key
        being an attribute of the submission (i.e. Title, Score, URL)
    """
    
    #initialize empty dictionary to store web-scraped results
    data = {}

    for submission in reddit.subreddit(sub).hot(limit=post_limit):
        #Make the key the submission id, store attributes of interest into a nested dictionary
        data[submission.id] = {'Title' : submission.title,
                                'score' : submission.score,
                                'upvote_ratio' : submission.upvote_ratio,
                                'num_comments' : submission.num_comments,
                                'url' : submission.url,
                                'text' : submission.selftext
                                }
    return data
    
reddit_dict = redditCrawler(reddit = reddit, sub = sub, post_limit = 100)

#Test print object
#reddit_dict['cdgfyg']['Title']

#Convert the dictionary into a pandas dataframe
df = pd.DataFrame.from_dict(reddit_dict, orient = 'index',
                       columns = ['Title','score','upvote_ratio','num_comments','url','text'])

print(df.columns)

