# -*- coding: utf-8 -*-
"""
Created on Jan 25th, 2021

@author: brian
From:
    http://www.storybench.org/how-to-scrape-reddit-with-python/

Look to scrape Wall Street Bets to see what is the most talked about stock that day
"""

import praw
from praw.models import MoreComments        
import re                                   #Regular Expressions for data cleanup
import config                               #passwords for account in another file

#log into Reddit
reddit = praw.Reddit(client_id=config.client_id, \
                     client_secret=config.client_secret, \
                     user_agent=config.user_agent, \
                     username=config.username, \
                     password=config.password)

# Enable read only mode
reddit.read_only = True

#convert a list of sentence to list of words
def convert(lst): 
    return ([i for item in lst for i in item.split()]) 

#look through 
def Top_Pics(input_list):
    #create a stock list
    stocks = []
    #convert inputs to a list of words
    output = convert(input_list)

    #loop through words  
    for word in output:
        #find words that are larger than 2 letters
        if len(word) > 2:
            #find words that are only upper case
            if word.isupper():
                #strip out unnecessary characters
                word = re.sub('\ |\?|\.|\!|\/|\;|\,|\$|\"', "", word)
                #add those words to possible stock pics
                stocks.append(word)
    
    #find top 40 stocks that day
    stock_dict = {i:stocks.count(i) for i in stocks}
    stock_dict_top = sorted(stock_dict, key=stock_dict.get, reverse=True)[:40]

    for stock in stock_dict_top:
        print(stock, stock_dict[stock])

def WSB_top_100():
    #search WSB subreddit
    subreddit = reddit.subreddit('wallstreetbets')
    
    #look for top 50 posts for the day
    top_subreddit = subreddit.top('day', limit=50)
    
    #create a list to strore comments
    comments_list = []
    
    #loop through posts and scrap all comments
    for submission in top_subreddit:
        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, MoreComments):
                continue
            #print(top_level_comment.body, '\n')    
            comments_list.append(top_level_comment.body)

    Top_Pics(comments_list)
    
if __name__ == '__main__':
    WSB_top_100()
