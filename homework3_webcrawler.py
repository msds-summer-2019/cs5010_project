#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Homework 3: Web Crawler
Names: Aditi Rajagopal, Bradley Katcher, Charlie Putnam
Computing-ID: ar5vt

"""

#libaries & imports
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Try out sentiment analysis with https://github.com/cjhutto/vaderSentiment
# pip install vaderSentiment 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# Feel free to comment out lines 18, 55 and 56 if you don't want sentiment analysis

# To Do:
#     something breaks when you try to get two different subreddit data maybe an issue with the way we are storing postDetails?


class SubRedditParse: 
    # fields: subreddit URL, sort-type [hot, new, top, controversial, rising] (defaults to hot), number of desired posts
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
            self.numPosts = 100
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
                timeStamp = timeStamp.replace("T", " ")
                timeStamp = timeStamp[:-6]

                # get sentiment score from post title
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

    # Psudoprettyprint:
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
            homepage = requests.get(self.URL, headers = {'User-agent': 'UVA DSI Bot Bob'})
            homePageSoup = BeautifulSoup(homepage.content, 'html.parser')
            homePageSoup.prettify()
            self.getPostDetails(homePageSoup.findAll("div", "top-matter"))
            try:
                nextLink = homePageSoup.find("span", "next-button")
                self.URL = nextLink.find("a")['href']
            except:
                break

    def getDataFrame(self):
        dataframe = pd.DataFrame(self.postDetails, columns=['title', 'source', 'postLink', 'author', 'postType', 'flair', 'timeStamp', 'sentimentScore'])
        return dataframe

CollegeBasketball = SubRedditParse("https://old.reddit.com/r/CollegeBasketball/", '', 50)
CollegeBasketball.redditCrawler()
CollegeBasketball.getDataFrame()
CollegeBasketball_df = CollegeBasketball.getDataFrame()
CollegeBasketball_df.to_csv('CollegeBasketball.csv')

CFB = SubRedditParse("https://old.reddit.com/r/CollegeBasketball/", '', 50)
CFB.redditCrawler()
CFB.getDataFrame()
CFB_df = CFB.getDataFrame()
CFB_df.to_csv('CFB.csv')

freeFolk = SubRedditParse("https://old.reddit.com/r/freefolk/", '', 50)
freeFolk.redditCrawler()
freeFolk_df = freeFolk.getDataFrame()

freeFolk_df.to_csv('freeFolk.csv')