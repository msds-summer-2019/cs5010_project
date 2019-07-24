#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 20:59:35 2019

@author: Bradley
"""
import pandas as pd

# import dataframe
df = pd.read_csv('uofm_osu.csv')


# Counts of Comments #
df.flair_clean.value_counts()

##### Raitings Graphs #########


#define the different raitings categories
raitings = ['neg', 'neu', 'pos', 'compound']

#loop through each of the raitings categories
for raiting in raitings:
    
    # give axis labels based on raiting
    if raiting == 'neg':
        y = "Negative Comment Raiting"
    if raiting == 'neu':
        y = "Neutral Comment Raiting"
    if raiting == 'pos':
        y = "Positive Comment Raiting"
    if raiting == 'compound':
        y = "Compound Comment Riating"
    
    # Make a separate list for each fan base
    x1 = list(df[df['flair_clean'] == 'neither'][raiting])
    x2 = list(df[df['flair_clean'] == 'michigan'][raiting])
    x3 = list(df[df['flair_clean'] == 'ohiostate'][raiting])
    
    # Assign colors for each fanbase and the names
    colors = ['#E69F00', '#56B4E9', '#F0E442']
    names = ['Neither', 'Michigan', 'Ohio State']
             
    # Make the histogram using a list of lists
    plt.hist([x1, x2, x3], bins = int(180/15), normed=False,
             color = colors, label=names)
    
    # Plot formatting
    plt.legend()
    plt.xlabel(str(y))
    plt.ylabel('Number of Comments')
    plt.title('Distrobution of Comment Sentiment by Fan Base')
    
    #plot exporting
    plt.savefig(str(raiting)+'.png')
    plt.clf()