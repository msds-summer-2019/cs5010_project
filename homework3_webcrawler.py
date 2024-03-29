#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Homework 3: Web Crawler
Names: Aditi Rajagopal, Bradley Katcher, Charlie Putnam
Computing-ID: ar5vt, bk5pu, cmp2cz
Note: Received permission from Professor Basit to work in a group of 3
"""

#libaries & imports
import requests
from bs4 import BeautifulSoup
import pandas as pd
# Try out sentiment analysis with https://github.com/cjhutto/vaderSentiment
# pip install vaderSentiment 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# Feel free to comment out lines 18, 55 and 56 if you don't want sentiment analysis

class SubRedditParse: 
    # Fields: subreddit URL, sort-type [hot, new, top, controversial, rising] (defaults to hot), number of desired posts
    # constructor:
    def __init__(self, URL, sortType, numPosts):
        if sortType:
            self.sortType = sortType
        else:
            self.sortType = ''
        self.URL = URL + self.sortType
        if numPosts:
            self.numPosts = numPosts
        else:
            self.numPosts = 100 #set default number of posts to 100
        self.postDetails = [];

    def __str__(self):
        return str(self.postDetails)

    # return post details
    def getPostDetails(self, posts):
        for post in posts:
            # title, source of post, direct link, type of post, author, author's flair
            try:
                postSource = post.find("span", "domain").text[1:-1]
                postTitle = post.find("a", "title may-blank").text
                postLink = self.URL + post.find("a", "title may-blank")['href'][6:]
                postType = post.find("span", "linkflairlabel")['title']
                author = post.select('a[class*="author may-blank id-"]')[0].text
                flair = post.select("span[class^=flair]")[0].text
                timeStamp = post.find("time", "live-timestamp")['datetime']
                # format time such that timestamp is convertable from UTC to desired timezone 
                timeStamp = timeStamp.replace("T", " ")
                timeStamp = timeStamp[:-6]
                # Get sentiment score from post title
                analyzer = SentimentIntensityAnalyzer()
                sentimentScore = analyzer.polarity_scores(postTitle)
                self.postDetails.append({
                    "title" : postTitle,
                    "source": postSource,
                    "postLink": postLink,
                    "author": author,
                    "postType": postType,
                    "flair": flair,
                    "timeStamp": timeStamp,
                    "sentimentScore": sentimentScore,
                })

    # Psudoprettyprint (included for debugging):
    #            print("Title: ", postTitle)
    #            print("Source: ", postSource)
    #            print("postLink: ", postLink)
    #            print("Author: ", author)
    #            print("Post Type: ", postType)
    #            print("Flair: ", flair)
    
            except:
                continue

    def redditCrawler(self):
        while len(self.postDetails) <= self.numPosts:
            # send header per reddit's api...will not work otherwise https://praw.readthedocs.io/en/v3.6.1/#a-few-short-examples
            homepage = requests.get(self.URL, headers = {'User-agent': 'UVA DSI Bot Bob'})
            # grab page content
            homePageSoup = BeautifulSoup(homepage.content, 'html.parser')
            homePageSoup.prettify()
            self.getPostDetails(homePageSoup.findAll("div", "top-matter"))
            try:
                nextLink = homePageSoup.find("span", "next-button")
                self.URL = nextLink.find("a")['href']
            except:
                break

    # return structured results into a dataframe
    def getDataFrame(self):
        dataframe = pd.DataFrame(self.postDetails, columns=['title', 'source', 'postLink', 'author', 'postType', 'flair', 'timeStamp', 'sentimentScore'])
        dataframe['timeStamp'] = pd.to_datetime(dataframe['timeStamp'])
        return dataframe


# Conduct the webscraping and put the data into a DataFrame
CFB = SubRedditParse("https://old.reddit.com/r/CFB/", '', 98)
CFB.redditCrawler()
cfb = CFB.getDataFrame()
cfb.to_csv('CFB.csv')   #exports results to a csv
# Make bar chart of frequency of Post Type
pt = cfb['postType'].value_counts().plot(kind='bar',
                                    figsize=(14,8),
                                    title="Post Type for r/CFB - Top 100")
pt.set_xlabel("Post Type")
pt.set_ylabel("Frequency")

# Obtain all flairs, split into multiple columns if there are multiple flairs, condense into one list and make that a dataframe
flair = cfb.flair.str.split(pat= " • " , n=-1, expand=True)
flair1 = flair[0]   #initial flair
flair2 = flair[1]   #secondary flair - displays as None if no flair exists
flair1.str.strip()
flair2.str.strip()
flairTot = flair1.append(flair2, ignore_index = True) #create one column with all flairs and then import that into a dataframe for anlaysis
flairTot = pd.DataFrame(data = flairTot, columns = ['flairs'])

# Make bar chart of Flairs
fl = flairTot['flairs'].value_counts().plot(kind='bar',
                                    figsize=(14,8),
                                    title="Most Frequent Flairs on Top 100 Posts")
fl.set_xlabel("Flair")
fl.set_ylabel("Frequency")

# Plot post frequency per hour
CFB_timestamps = cfb[cfb.columns[6]]
CFB_timestamps.groupby(CFB_timestamps.dt.hour).count().plot(kind="bar")
