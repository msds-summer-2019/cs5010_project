"""

CS5010: Final Project
Names: Aditi Rajagopal, Bradley Katcher, Charlie Putnam
Computing-ID: ar5vt, bk5pu, cmp2cz
Content: Pull data from reddit using RedditPostParse, store in csv, and generate pretty visuals
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

from final_project_praw import RedditPostParse


#Get first half of data from thread 1
uofm_osu_firsthalf = RedditPostParse("https://www.reddit.com/r/CFB/comments/9zzk5n/game_thread_michigan_ohio_state_1200pm_et/", 'michigan', 'ohiostate')
uofm_osu_firsthalf.getComments()
uofm_osu_firsthalf_df = uofm_osu_firsthalf.getDataFrame()

#Get second half of data from thread 2
uofm_osu_secondhalf = RedditPostParse("https://www.reddit.com/r/CFB/comments/a018xs/game_thread_michigan_ohio_state_1200pm_et_second/", 'michigan', 'ohiostate')
uofm_osu_secondhalf.getComments()
uofm_osu_secondhalf_df = uofm_osu_secondhalf.getDataFrame()

#Concatenate dataframes together into one
uofm_osu = pd.concat([uofm_osu_firsthalf_df, uofm_osu_secondhalf_df])

#Write result to csv
uofm_osu.to_csv('uofm_osu.csv') #exports results to a csv

#Convert author to string so we can sort later
uofm_osu['author'] = uofm_osu['author'].astype(str)

#Pivot the data to create column groups: flair1, flair2, and others
uofm_osu = uofm_osu.pivot_table(index = ['timeStamp','author'], columns = 'flair_clean',
               values = 'compound', aggfunc = ['count','mean'])

#Collapse the multi-column index to single level
uofm_osu.columns = uofm_osu.columns.map('|'.join).str.strip('|')

#Drop author from index
uofm_osu = uofm_osu.droplevel('author')

#Resample into 5 minute bins and calculate average sentiment over that time
uofm_osu.resample('5T').mean().to_csv('average_sentiment_over_time.csv')

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
