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

def get_next_urlSuffix(soup, urlPrefix):
    pattern = re.compile('Next')
    for a in soup.find_all('a', text=pattern):
        urlReturn = a['href']
        break
    retrurn
    
    
    
    
    


if __name__ == "__main__":
    path = str(os.path.dirname(os.path.realpath(__file__)))+'/data/'
    urlPrefix = 'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/'
    urlSuffix = 'viewtopic.php?t=12591'
    url = urlPrefix+urlSuffix
    
    soup = get_soup(url)
    
    nurlSuffix = get_next_urlSuffix(soup, urlPrefix)
    
    