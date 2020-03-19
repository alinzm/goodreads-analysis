
# coding: utf-8

# In[1]:


#Gathering user groups data from goodreads
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen
from urllib.error import URLError
import time
import random
from tqdm import tqdm


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
import re
import math
import os.path

#
start = time.time()
count = 1
##
###Select the Number of Users

number_of_users = 5

##
###introduce the chrome Driver --> Download your version from here:
###https://chromedriver.chromium.org/downloads
##
options = Options()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized') # 
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(chrome_options=options, executable_path='/root/goodreads/chromedriver_linux')



##
##
##
pbar = tqdm(total = number_of_users)
while count < number_of_users+1:
    
    #Pick User Ids Randomly
    userid = random.randint(1000000,20000000)
    #userid = 82076273
    
    
#    #Get the Initial Data from User
    try:
        user_req = Request("https://www.goodreads.com/user/show/{}.xml?key=******API KEY*******".format(userid))
        user_response = urlopen(user_req)
        user_tree = ET.parse(user_response)
        user_shelves_count = user_tree.findall('.//reviews_count')[0].text
        
        
        #Check if User has specific Number of Books in his(her) shelves
        if int(user_shelves_count) > 1: 
#
#            
            user_name = user_tree.findall('.//name')[0].text
            user_gender = user_tree.findall('.//gender')[0].text
            user_location = user_tree.findall('.//location')[0].text
            user_joined = user_tree.findall('.//joined')[0].text
            user_about = user_tree.findall('.//about')[0].text
            user_image_url = user_tree.findall('.//image_url')[0].text
            
#        
            #Get the user Review and Rating Count by Scraping with soup and selenium
            driver.get('https://www.goodreads.com/user/show/{}'.format(userid))

            time.sleep(4)
            try:
                xpath1 = "/html/body/div[3]/div/div/div[1]/button"
                close_popup = driver.find_element_by_xpath(xpath1)
                close_popup.click()
            except:
                pass
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            profilePageUserStatsInfo = soup.find('div', {'class':'profilePageUserStatsInfo'})
            user_ratings = []
            for data in profilePageUserStatsInfo.find_all('a'):
                user_ratings.append(data.text)
            
            user_rating = str(user_ratings[0]).split(' ')[0]
            user_review = str(user_ratings[2]).split(' ')[8]
#    
            #Create final User_info list
            user_info = []
            #user_info.append([userid,user_name,user_gender,user_location,user_joined,user_shelves_count,user_about,user_image_url])
            user_info.append([userid,user_name,user_gender,user_location,user_rating,user_review,user_joined,user_shelves_count,user_about,user_image_url])
            
#            
            #Add user data to the CSV --> Append to previous CSV if exists
            file_exists = os.path.isfile('/root/goodreads/users.csv')
            header = ['userid','user_name','user_gender','user_location','user_rating','user_review','user_joined','user_shelves_count','user_about','user_image_url']
            with open('/root/goodreads/users.csv', 'a', newline ='') as file:
                writer = csv.writer(file, delimiter=',')
                if file_exists != True:
                    writer.writerow(i for i in header)
                for j in user_info:
                    writer.writerow(j)

#                
            #Request the number of Books in Read shelves for each User
            review_req = Request("https://www.goodreads.com/review/list/{}.xml?key=******API KEY*******&v=2&shelf=read&per_page=5".format(userid))
            user_review = urlopen(review_req)
            review_tree = ET.parse(user_review)
            user_review = (review_tree.findall('.//reviews')[0].attrib)['total']


            #Loop over the books in the Read Shelves and create page_numbers
            #Maximum number of books for each request is 200 books, we must loop over pages
            for page_numer in range (1,math.ceil(int(user_review)/200)+1):
                time.sleep(1)  
#            
                try:
                    req = Request("https://www.goodreads.com/review/list/{}.xml?key=******API KEY******* &v=2&shelf=read&per_page=200".format(userid)+"&page="+str(page_numer))
                    response = urlopen(req)
                    tree = ET.parse(response)
                    root = tree.getroot()

#                    
                    #Get the data for each Book
                    user_books = []
                    book_number = 0
                    for user in root.iter('review'):
                        book_number = book_number + 1
                        book = user.find('./book/title_without_series').text
                        pub_year = user.find('./book/publication_year').text
                        rating = user.find('./book/average_rating').text
                        rating_count = user.find('./book/ratings_count').text
                        description = user.find('./book/description').text
                        author = user.find('./book/authors/author/name').text
                        author_id = user.find('./book/authors/author/id').text
                        user_book_review = user.find('./body').text                   
                        user_books.append([userid,book,pub_year,rating,rating_count,description,user_book_review,author,author_id]) 
                        #print ("User: {} | Total Users: {} | Book Numer: {} | Total Number of User Books: {} | Time Passed: {}".format(count, number_of_users,book_number,user_review,((time.time() - start)/60)),end="\r")
                    
                #In case the page doesn't exists
                except:
                    pass
#                
            count = count + 1
            pbar.update(1)
#            #Add user data to the CSV --> Append to previous CSV if exists
            
            file_exists = os.path.isfile('/root/goodreads/userBooks.csv')
            header = ['userid','book','pub_year','rating','rating_count','description','user_book_review','author','author_id']
            with open('/root/goodreads/userBooks.csv', 'a', newline ='') as file:
                writer = csv.writer(file, delimiter=',')          
                if file_exists != True:
                    writer.writerow(i for i in header)
                for j in user_books:
                    writer.writerow(j)
            #print ("hello")         
    #In case the user doesn't exists             
    except:
        pass
    
#
#
#driver.quit()
#        
##
