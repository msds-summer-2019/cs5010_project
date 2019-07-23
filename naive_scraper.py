#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 15:02:40 2019

@author: Bradley
"""

import praw
import pandas as pd

reddit = praw.Reddit(client_id='vuPSE6ZQtZR5Aw',
                     client_secret='vBP2bxfwsr3c_BdmJjzUpZapwtU',
                     user_agent='my user agent')

submission = reddit.submission(id = 'cgea2o')
 
results = { "text":[], "user":[], "submitter":[], "score":[], "time":[], "permalink":[], "flairs":[], "len":[]}


for comment in submission.comments:
    results["text"].append(comment.body)
    results["user"].append(comment.author)
    results["submitter"].append(comment.is_submitter)
    results["score"].append(comment.score)
    results["time"].append(comment.created_utc)
    results["permalink"].append(comment.permalink)
    x = len(comment.replies)
    
        for reply in comment.replies:
            results["text"].append(reply.body)
            results["user"].append(reply.author)
            results["submitter"].append(reply.is_submitter)
            results["score"].append(reply.score)
            results["time"].append(reply.created_utc)
            results["permalink"].append(reply.permalink)
    
scraped = pd.DataFrame.from_dict(results, orient='index')
scraped = scraped.transpose()
    
    
