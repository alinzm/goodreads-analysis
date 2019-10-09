## Goodreads Analysis


This repository is dedicated to crawling and analysing the data from the social media [Goodreads](https://goodreads.com).

### Crawling the Data

Goodread's Data is accessible through XML files. You need to get your API key. The piece of code here, is a very Basic version which make requests to the API and save the Data from XML file in to CSV format.

The user's ID is used to access the books he/she listed as **READ BOOKS** and the Book's ID is used to gather the Data of the Book's Author. The final CSV file is like this: 

| UserId        | Name of The Book           | Author  |Publish Year   | Book Ranking|Number of Fans| Number of Books| City| Gender
| ------------- |:-------------:| -----:|-----:|-----:|-----:|-----:|-----:|-----:|
| 19574305     |Starters  | Lissa Price	 | 2012| 3.91| 1622 | 10 | California| Female

### Social Network Analysis on the Books and the Users
