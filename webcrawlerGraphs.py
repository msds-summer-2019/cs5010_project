#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 09:06:14 2019

@author: Bradley
"""

# conduct the webscraping and put the data into a DataFrame
CFB = SubRedditParse("https://old.reddit.com/r/CFB/", '', 98)
CFB.redditCrawler()
cfb = CFB.getDataFrame()

#Make bar chart of Post Type
pt = cfb['postType'].value_counts().plot(kind='bar',
                                    figsize=(14,8),
                                    title="Post Type for r/CFB - Top 100")
pt.set_xlabel("Post Type")
pt.set_ylabel("Frequency")
pt.show()

# Obtain all flairs, split into multiple columns if there are multiple flairs, condense into one list and make that a dataframe
flair = cfb.flair.str.split(pat= " • " , n=-1, expand=True)
flair1 = flair[0]
flair2 = flair[1]
flair1.str.strip()
flair2.str.strip()
flairTot = flair1.append(flair2, ignore_index = True) 
flairTot = pd.DataFrame(data = flairTot, columns = ['flairs'])


#Make bar chart of Flairs
fl = flairTot['flairs'].value_counts().plot(kind='bar',
                                    figsize=(14,8),
                                    title="Most Frequent Flairs on Top 100 Posts")
fl.set_xlabel("Flair")
fl.set_ylabel("Frequency")
