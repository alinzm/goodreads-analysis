
# coding: utf-8

# In[460]:


#Gathering user groups data from goodreads
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen
from urllib.error import URLError
import time
import pandas as pd
import random
from tqdm import tqdm

#test_
goodreads_users = []
not_found = 0
found = 0
count = 0
time_all = 0

while count < 5:
    start = time.time()
    userid = random.randint(19000000,20000000)
    
    req = Request("https://www.goodreads.com/review/list/{}.xml?key=&v=2&shelf=read&per_page=200".format(userid))
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print ("user "+str(userid)+" is not valid")
        elif hasattr(e, 'code'):  
            print ("user "+str(userid)+" is not valid")
    else:
        count = count +1
        for page_numer in range (1,20):
            req = Request("https://www.goodreads.com/review/list/{}.xml?key=&v=2&shelf=read&per_page=200".format(userid)+"&page="+str(page_numer))
            try:
                response = urlopen(req)
            except URLError as e:
                if hasattr(e, 'reason'):
                    print ("page "+str(page_numer)+" is not valid")
                    not_found = not_found +1
                elif hasattr(e, 'code'):
                    print ("page "+str(page_numer)+" is not valid")
                    not_found = not_found +1
            else:
                tree = ET.parse(response)
                root = tree.getroot()
                found = found +1
            
                for user in root.iter('review'):
                    book = user.find('./book/title_without_series').text
                    pub_year = user.find('./book/publication_year').text
                    rating = user.find('./book/average_rating').text
                    author = user.find('./book/authors/author/name').text
                    author_id = user.find('./book/authors/author/id').text
        
                    author_req = Request("https://www.goodreads.com/author/show/{}?format=xml&key=".format(author_id))
                    response = urlopen(author_req)
                    tree = ET.parse(response)
                    root = tree.getroot()
                    for author_info in root.iter('fans_count'):
                        author_fan = author_info.text
                    for author_info in root.iter('works_count'):
                        author_books = author_info.text
                    for author_info in root.iter('hometown'):
                        author_hometown = author_info.text
                    for author_info in root.iter('gender'):
                        author_gender = author_info.text
                    time.sleep(1)       
                    goodreads_users.append([userid,book,author,pub_year,rating,author_fan,author_books,author_hometown,author_gender])  
                    
            goodreads_network = pd.DataFrame(goodreads_users)
            with open('/Users/choobani/Desktop/userBooks.csv', 'a') as final_users:
                goodreads_network.to_csv(final_users, mode='a',header=False, index=False)         
            goodreads_users = []
            
        time.sleep(1)
        end = time.time()
        time_all = time_all + (end-start)
    
    
print (str(time_all/60)+" Minutes to crawl "+str(count)+" users")
print ("From "+ str(found+not_found)+" pages "+str(not_found)+" Pages are not Found.")

