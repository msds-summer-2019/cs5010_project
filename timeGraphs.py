#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:57:31 2019

@author: Bradley
"""



import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime
import pandas as pd

#df = df.loc[df['flair_clean'] == 'ohiostate']
        
df = pd.read_csv('uofm_osu.csv')
df.drop(df.tail(3).index,inplace=True)
df = df.loc[df['flair_clean'] == 'ohiostate']

df['timeStamp'] = df['timeStamp'].apply(lambda x : pd.to_datetime(str(x)))
df['times'] = df['timeStamp'].dt.time
df['comnumber'] = np.arange(len(df))

# create data
x = df['times']
y = df['comnumber']

# plot
plt.plot(x,y, "o")
plt.xlabel('Time')
plt.ylabel('Number of Comments')
plt.title('Number of Comments over Time: Ohio State')



