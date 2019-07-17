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

# To Do:
#     store scraped/parsed data into a dataframe


class SubRedditParse: 
    # fields: subreddit URL, sort-type [hot, new, top, controvercial, rising] (defaults to hot), number of desired posts
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
        self.dataFrame = pd.DataFrame(columns=['title', 'source', 'postLink', 'author', 'postType', 'flair'])

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
                
                newPostDetails = {
                    "title" : postTitle,
                    "source": postSource,
                    "postLink": postLink,
                    "author": author,
                    "postType": postType,
                    "flair": flair
                }
                
                # 60 & 61 don't work
                self.postDetails.append(newPostDetails)
                self.dataFrame = self.dataFrame.append(newPostDetails)
    
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

    # this doesn't work
    def storeNprintDataFrame(self):
#        self.dataFrame = pd.DataFrame(columns=['title', 'source', 'postLink', 'author', 'postType', 'flair'])
        self.dataFrame = pd.DataFrame(self.postDetails)
        print(self.dataFrame)
#        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#            print(self.dataFrame)
    
BiglittleLies = SubRedditParse("https://old.reddit.com/r/biglittlelies/", 'top', 10)
BiglittleLies.redditCrawler()
BiglittleLies.storeNprintDataFrame()


rCFB = SubRedditParse("https://old.reddit.com/r/CFB", 'new', 50)
rCFB.redditCrawler()
rCFB.storeNprintDataFrame()
