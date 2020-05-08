
# coding: utf-8

# In[2]:


#Gathering user groups data from goodreads
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen
from urllib.error import URLError
import time
import pandas as pd
import random
from tqdm import tqdm_notebook


from bs4 import BeautifulSoup
import requests 
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import urlsplit
import pandas as pd
import re
import math
import os.path

import csv


# In[3]:


#Provide a list of Author IDs
authors_dataset = pd.read_csv("Author_ids.csv", header=0, names=["id"])


# In[4]:


#Access Gooread's API for Each Author 
def get_author_data(authorid):

        author_req = Request("https://www.goodreads.com/author/show/{}?format=xml&key=--------API KEY--------".format(authorid))
        response = urlopen(author_req)
        tree = ET.parse(response)
        root = tree.getroot()
    
        name = root.find(".author/name").text
        fan_count = root.find(".author/fans_count").text
        followers_count = root.find(".author/author_followers_count").text
        hometown = root.find(".author/hometown").text
        gender = root.find(".author/gender").text
        big_image = root.find(".author/large_image_url").text
        about = root.find(".author/about").text
        born = root.find(".author/born_at").text
        died = root.find(".author/died_at").text
        workcount = root.find(".author/works_count").text
        influence = None
        
        try:
            influence_soup = BeautifulSoup(root.find(".author/influences").text, 'html.parser')
            influence = ""
            for a in influence_soup.find_all('a'):
                influence = a.text  +","+ influence
        except:
            pass

        
        authorinfo = [authorid,name,workcount,fan_count, followers_count,hometown,gender,big_image,about,born,died,influence]
        authorinfo.extend(get_author_details(authorid))
        return (authorinfo)    
    


# In[5]:


#Access Author's page with Chromes Driver and scrap the inaccessible with the API

def get_author_details(authorid):
    
    driver.get('https://www.goodreads.com/author/show/{}'.format(authorid))
    
    time.sleep(4)
    try:
        xpath1 = "/html/body/div[3]/div/div/div[1]/button"
        close_popup = driver.find_element_by_xpath(xpath1)
        close_popup.click()
    except:
        pass
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
        
    time.sleep(4)
    try:
        xpath1 = "/html/body/div[3]/div/div/div[1]/button"
        close_popup = driver.find_element_by_xpath(xpath1)
        close_popup.click()
    except:
        pass
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')


    profile_data = soup.find('div', {'class':'rightContainer'})


    reviews = soup.find('div', {'class':'hreview-aggregate'})
    average_rate = (reviews.find('span', {'class':'average'}).text.replace("\n",""))
    rating_count = (reviews.find('span', {'class':'votes'}).text.replace("\n",""))
    review_count = (reviews.find('span', {'class':'count'}).text.replace("\n",""))
    books_in_goodreads = (reviews.find_all('a')[0].text.replace(" distinct works",""))
    
    website = "no-website"
    twitter = "no-twitter"
    Genre = "no-Genre"


    for div in soup.find_all('div'):
        if div.text == "Website":
            website = (div.find_next_sibling("div").text.replace("\n",""))
        
        elif div.text == "Twitter":
            twitter = (div.find_next_sibling("div").text.replace("\n",""))

        elif div.text == "Genre":
            Genre = (div.find_next_sibling("div").text.replace("\n",""))


    return ([average_rate, rating_count, review_count, books_in_goodreads, Genre, website, twitter])


# In[6]:


def write_to_csv(file_path, header, data):
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        if file_exists != True:
            writer.writerow(i for i in header)
        writer.writerow(data)


# In[ ]:


#Change Driver Path
driver = webdriver.Chrome('chromedriver')

#Change final CSV file Path
author_csv_file_path = 'authors.csv'

header = ['authorid','name','workcount','fan_count', 'followers_count','hometown',
          'gender','big_image','about','born','died','influence','average_rate',
          'rating_count', 'review_count', 'books_in_goodreads', 'Genre', 'website', 'twitter']

for i in tqdm_notebook(range(len(authors_dataset))):
    try:
        write_to_csv(author_csv_file_path, header, get_author_data(authors_dataset['id'].iloc[i]))
    except:
        continue

