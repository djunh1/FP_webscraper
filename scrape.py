# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 18:46:23 2016

@author: djunh
"""

import re
import os

import pandas as pd
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
    
    print()
    
    indexValue = 1
    for idx,value in enumerate(body_details):
       if value.getText() == '':
           pass
       else:
          
           print(indexValue, value.getText())
           #df.ix[indexValue]['body'] = value.getText();
           indexValue +=1
    return df

if __name__ == "__main__":
    path = str(os.path.dirname(os.path.realpath(__file__)))+'/data/'
    
    fields = ['post_id', 'name', 'date', 'body']
    
    
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
        
    extract_data(urlTest)

    # urlList is populated, collect data and append dataframe with each
    # Pages post information
    '''
    for url in urlList:
        print("Extracting data from the url - " + url)
        dfNew = extract_data(url)
        #df = pd.concat(df, dfNew)
    '''   
        
