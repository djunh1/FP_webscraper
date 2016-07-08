# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 18:46:23 2016

@author: djunh
"""

import re
import os
import sys

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urllib


def get_soup(url):
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)
    return soup


def get_next_url(soup):
    '''
    Returns a new URL based on the curent URLs links.  Used to loop through
    and entire threads posts
    
    Arguements:
    soup - a soup 
    '''
    urlReturn =''
    pattern = re.compile('Next')
    for a in soup.find_all('a', text=pattern):
        urlReturn = a['href']
        break
    return urlReturn
    #Returns none if empty
    

def extract_data(url):
    '''
    Extracts all data from a specific url following conventions of posts
    on the site.  
    
    Arguements:
    url -  the page URL to scrape.  Must be a full URL with domain
    df - the dataframe to be populated and returns
    
    TODO -  A more robust method to index actual posts vs quotes ( which 
    have no text nodes)
    '''
    
    soup = get_soup(url)
    df = pd.DataFrame(columns = fields, index = range(1,16))
    dfBody = pd.DataFrame(columns = ['body'], index = range(1,40))
    #Get post_id data, input into a dataframe
    pattern = re.compile('[0-9]')
    post_id_details = soup.find_all('a',{"name":True})
    for idx, value in enumerate(post_id_details):
        if re.match(pattern, value['name']):        
            df.ix[idx]['post_id'] = value['name']
            
    #Get name of post, input into dataframe
    name_details = soup.find_all('span', {"class": 'name'})
    for idx,value in enumerate(name_details):
        df.ix[idx+1]['name'] = value.find('b').getText()
    
    #Get Date of post
    for idx, value in enumerate(soup(text=re.compile('Posted:'))):
        df.ix[idx+1]['date'] = value.parent.getText()[7:][:26]

    #Get Body of Post
    body_details = soup.find_all('span', {"class": 'postbody'})
    indexValue = 1
    for idx,value in enumerate(body_details):
       if value.getText() == '':
           pass
       else:
           dfBody.ix[indexValue]['body'] = value.getText()
           indexValue +=1
           
    dfNew = dfBody.drop_duplicates().reset_index(drop = True)
    dfNew.index = range(1,len(dfNew)+1)
    df['body'] = dfNew
    return df
   
   
def clean_data(df):
    
    df = df.reset_index(drop = True).dropna()
    return df
    
    
def data_to_csv(df):
    filePathString = path + 'forum.csv'
    df.to_csv(filePathString)

if __name__ == "__main__":
    path = str(os.path.dirname(os.path.realpath(__file__)))+'/data/'
    reload(sys)
    sys.setdefaultencoding('utf-8')
    fields = ['post_id', 'name', 'date', 'body']
    df = pd.DataFrame(columns = fields)
    
    url = 'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591'
    urlList = [url]

    #Generate list of URLs.  Will break as soon as no new URL is present
    soup = get_soup(url)

    while True:
        newUrlSuffix = get_next_url(soup)
        if newUrlSuffix == '':
            break
        newUrl = 'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/' + newUrlSuffix
        print("Adding new URL to list..")
        urlList.append(newUrl)
        soup = get_soup(newUrl)

    # urlList is populated, collect data and append dataframe with each
    # Pages post information
     
    dft = extract_data('http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591&postdays=0&postorder=asc&start=75&sid=efa57f3533e503c2622eb82e82e546d4')

   
    for link in urlList:
        print("Extracting data from the url - " + link + '\n\n\n')
        dfNew = extract_data(link)
        df = pd.concat([df, dfNew])

    dfCleaned = clean_data(df)
    data_to_csv(dfCleaned)
    