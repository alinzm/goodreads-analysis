## Goodreads Analysis


This repository is dedicated to crawling and analyzing the data from social media [Goodreads](https://goodreads.com). Social Network analysis on the Users of the goodreads would provide us with a better understanding of the user's behavior in reading. 

### Crawling the Data

Goodread's Data is accessible through XML files. You need to get your API key. The piece of code here is a basic version which makes requests to the API and save the Data from the XML file into CSV format.

The user's ID is used to access the books he/she listed as **READ BOOKS**, and the Book's ID is used to gather the Data of the Book's Author. By making some minor changes, we can also access the **Currently-Reading** or **To-Read**. The final CSV file is like this: 

| UserId        | Name of The Book           | Author  |Publish Year   | Book Ranking|Number of Fans| Number of Books| City| Gender
| ------------- |:-------------:| -----:|-----:|-----:|-----:|-----:|-----:|-----:|
| 19574305     |Starters  | Lissa Price     | 2012| 3.91| 1622 | 10 | California| Female

The Only limitation in crawling data from Goodreads is time. The service doesn't let developers make requests in less than 1 seconds each time, this can be solved by running the code in parallel. Crawling 107,438 rows of Data (nearly 14,000 users) took 3 days. 

### Social Network Analysis on the Books and the Users

To be added soon. 
