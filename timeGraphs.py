#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:57:31 2019

@author: Bradley
"""


#import libraries for graph creation
import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, date
import pandas as pd


def minsGraph(fanbase):
    #import data and remove three outliers        
    df = pd.read_csv('uofm_osu.csv')
    df.drop(df.tail(3).index,inplace=True)
    
    #restrict data to fanbase
    if fanbase == 'all':
        df = df
    if fanbase != 'all':
        df = df.loc[df['flair_clean'] == fanbase]

    df['start_time'] = "2018-11-24 11:00:00"
    df['start_time'] = pd.to_datetime(df['start_time'], format='%Y-%m-%d %H:%M:%S')
    
    
    df['timeStamp'] = df['timeStamp'].apply(lambda x : pd.to_datetime(str(x)))
    df['times'] = df['timeStamp'].dt.time
    
    df['comnumber'] = np.arange(len(df))
    
    df['diff_mins'] = df['timeStamp'] - df['start_time']
    df['diff_mins']=df['diff_mins']/np.timedelta64(1,'m')
    
    # create data
    x = df['diff_mins']
    y = df['comnumber']
    
    # plot
    plt.plot(x,y, "o")
    plt.xlabel('Time')
    plt.ylabel('Number of Comments')
    plt.title('Number of Comments over Time: ' +str(fanbase))

def timeGraph(fanbase):
    #import data and remove three outliers        
    df = pd.read_csv('uofm_osu.csv')
    df.drop(df.tail(3).index,inplace=True)
    
    #restrict data to fanbase
    if fanbase == 'all':
        df = df
    if fanbase != 'all':
        df = df.loc[df['flair_clean'] == fanbase]
    
    df['start_time'] = "2018-11-24 11:00:00"
    df['start_time'] = pd.to_datetime(df['start_time'], format='%Y-%m-%d %H:%M:%S')
    
    
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
    plt.title('Number of Comments over Time: ' +str(fanbase))



