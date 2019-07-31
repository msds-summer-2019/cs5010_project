#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 16:32:58 2019

@author: Bradley
"""
#import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# function to compute the correltation between a given 
def corr(category, sentiment):
    df = pd.read_csv('uofm_osu.csv') #read in csv of scraped data
    
    if category == 'all': # if all, don't subset data, just compute correlation
        return np.corrcoef(df.votes,df[sentiment])
    else: 
        df = df.loc[df['flair_clean'] == category] #subset by fanbase
        return np.corrcoef(df.votes, df[sentiment])

#function to create a scatterplot showing number of votes by your choice of sentiment score
def graph(category, sentiment):
    df = pd.read_csv('uofm_osu.csv')
    df['log_votes'] = np.log(df['votes'])
    
    if category == 'all': # if all, don't subset data
        plt.scatter(df[sentiment],df.votes)
        plt.xlabel("Sentiment Score")
        plt.ylabel("Number of Up-votes")
        return plt.show()
    else: 
        df = df.loc[df['flair_clean'] == category] #subset by fanbase
        plt.scatter(df[sentiment],df.votes)
        plt.xlabel("Sentiment Score")
        plt.ylabel("Number of Up-votes")
        return plt.show()
    
### Make Graphs
    graph('all','compound')
    graph('michigan', 'compound')
    graph('ohiostate', 'compound')


### Summary Stats
    def mean(mArg):
        df = pd.read_csv('uofm_osu.csv')
        return df.groupby(mArg).mean()
            
    mean('flair_clean')
    
### Compute correlations:
    corr('michigan','compound')
    corr('neither', 'compound')
    corr('ohiostate', 'compound')
