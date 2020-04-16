
# coding: utf-8

# In[1]:


# Gathering user groups data from goodreads
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen
from urllib.error import URLError
import time
import random
from tqdm import tqdm
import sys

from bs4 import BeautifulSoup
import requests
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


start = time.time()
count = 1

# Select the Number of Users
number_of_users = 5

# put your api key here
GOODREADS_API_KEY = '******API KEY*******'

# put your chromedriver here
CHROME_WEBDRIVER_EXECUTABLE_PATH = '/usr/local/bin/chromedriver'

output_dir = 'goodreads'
user_csv_file_path = os.path.join(output_dir, 'users.csv')
user_books_csv_file_path = os.path.join(output_dir, 'userBooks.csv')

# introduce the chrome Driver --> Download your version from here:
# https://chromedriver.chromium.org/downloads
options = Options()
options.add_argument("--headless")  # Runs Chrome in headless mode.
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(chrome_options=options,
                          executable_path=CHROME_WEBDRIVER_EXECUTABLE_PATH)


def check_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def write_to_csv(file_path, header, data):
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        if file_exists != True:
            writer.writerow(i for i in header)
        for j in data:
            writer.writerow(j)


def make_api_request(url):
    req = Request(url)
    response = urlopen(req)
    return ET.parse(response)


def get_user_info(userid):
    try:
        user_tree = make_api_request(
            "https://www.goodreads.com/user/show/{}.xml?key={}".format(userid, GOODREADS_API_KEY))

        user_shelves_count = user_tree.findall('.//reviews_count')[0].text
        # Check if User has specific Number of Books in his(her) shelves
        if int(user_shelves_count) > 1:
            user_name = user_tree.findall('.//name')[0].text
            user_gender = user_tree.findall('.//gender')[0].text
            user_location = user_tree.findall('.//location')[0].text
            user_joined = user_tree.findall('.//joined')[0].text
            user_about = user_tree.findall('.//about')[0].text
            user_image_url = user_tree.findall('.//image_url')[0].text

            # Get the user Review and Rating Count by Scraping with soup and selenium
            driver.get('https://www.goodreads.com/user/show/{}'.format(userid))

            time.sleep(4)
            try:
                xpath1 = "/html/body/div[3]/div/div/div[1]/button"
                close_popup = driver.find_element_by_xpath(xpath1)
                close_popup.click()
            except:
                pass

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            profilePageUserStatsInfo = soup.find(
                'div', {'class': 'profilePageUserStatsInfo'})
            user_ratings = []
            for data in profilePageUserStatsInfo.find_all('a'):
                user_ratings.append(data.text)

            user_rating = str(user_ratings[0]).split(' ')[0]
            user_review = str(user_ratings[2]).split(' ')[8]
            return [[userid, user_name, user_gender, user_location, user_rating,
                     user_review, user_joined, user_shelves_count, user_about, user_image_url]]
        return None
    except:
        return None


def get_user_books(userid):
    user_books = []
    # Request the number of Books in Read shelves for each User
    review_tree = make_api_request(
        "https://www.goodreads.com/review/list/{}.xml?key={}=&v=2&shelf=read&per_page=5".format(userid, GOODREADS_API_KEY))
    user_review = (review_tree.findall(
        './/reviews')[0].attrib)['total']
    # Loop over the books in the Read Shelves and create page_numbers
    # Maximum number of books for each request is 200 books, we must loop over pages
    for page_numer in range(1, math.ceil(int(user_review)/200)+1):
        time.sleep(1)

        try:
            tree = make_api_request("https://www.goodreads.com/review/list/{}.xml?key={}&v=2&shelf=read&per_page=200".format(
                userid, GOODREADS_API_KEY)+"&page="+str(page_numer))
            root = tree.getroot()

            # Get the data for each Book
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
                user_books.append(
                    [userid, book, pub_year, rating, rating_count, description, user_book_review, author, author_id])
                # print ("User: {} | Total Users: {} | Book Numer: {} | Total Number of User Books: {} | Time Passed: {}".format(count, number_of_users,book_number,user_review,((time.time() - start)/60)),end="\r")

        # In case the page doesn't exists
        except:
            pass
    return user_books


check_dir(output_dir)

pbar = tqdm(total=number_of_users)
while count < number_of_users+1:

    # Pick User Ids Randomly
    userid = random.randint(1000000, 20000000)

    # Get the Initial Data from User
    try:
        user_info = get_user_info(userid)
        if user_info == None:
            continue

        user_books = get_user_books(userid)
        if user_books == None or len(user_books) == 0:
            continue

        # Add user data to the CSV --> Append to previous CSV if exists
        header = ['userid', 'user_name', 'user_gender', 'user_location', 'user_rating',
                  'user_review', 'user_joined', 'user_shelves_count', 'user_about', 'user_image_url']
        write_to_csv(user_csv_file_path, header, user_info)

        # Add user data to the CSV --> Append to previous CSV if exists
        header = ['userid', 'book', 'pub_year', 'rating', 'rating_count',
                  'description', 'user_book_review', 'author', 'author_id']
        write_to_csv(user_books_csv_file_path, header, user_books)

        count = count + 1
        pbar.update(1)

    # In case the user doesn't exists
    except:
        pass


driver.quit()

##
