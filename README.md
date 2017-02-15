Web Scraper that scraps information from any wikipedia category, outputs json file of scraped material and allows you to search the information.

-----------------------
COMMAND LINE ARGUMMENTS
-----------------------

./install.sh-----> To install scrapy. (Make sure python 2.x and pip are installed)
./download.sh "list_of_categories.txt" -----> To scrape all the categories from list_of_categories text file. All the scrape results are stored in items.txt file.
./search.sh "query_thing_you_want_to_search_for" "yes/no option_to_display_text or letter of wikipedia category" -----> eg: ./search.sh "machine learning" "no". Displays top 5 results based on tfidf ranking.


-------------------------------------
DESIGN DECISIONS AND SOME EXPLANATION
-------------------------------------


PART 1 ----- DATA COLLECTION

* What is it?

This webcrawler is built on an open source web scraping framework called Scrapy (http://scrapy.org/). 

* Why Scrapy?
	- Easy to use and great documentation
	- Support for proxies, authentication, cookies
	- Scalability. Companies like careerbuilder, parse.ly and data.gov.uk are using scrapy. 
	- Easy to export data in text,json, csv or xml
	- Great testing and debugging capabilities

Installation:
* Make sure python 2.x and pip are installed
* ./install.sh to install scrapy


Model for data collection

items
Selectors
Spiders
Item Pipeline
Being nice and not getting IP banned 
	-robots.txt
	-DOWNLOAD_DELAY
	-USER_AGENT


1) items.py - Things we want after crawling. That is where we define the models of scraped items. It is a thin layer over python. Sometimes we can use this to preprocess and validate data. 


2) Selectors - To select elements/data from HTML source. Scrapy has two ways to select data - XPath and CSS. I have used both in my crawler. It is built over an lxml library. 


3) Spiders (crawler_1 to crawler_5.py) - Brain of the project. Logic on how to parse the website. First we define the start url. Then we do a depth first search or a breadth first search.The cool thing about scrapy is we can set a depth limit so that we can stop at a particular limit. The most important question to ask here is to whether we need to do a "focused crawl" or a "broad crawl". Focused crawl is suituable if we have few websites to scrape where as broad crawl is for when there is a lot (thousands or millions of sites to scrape). Focused crawl is implemented here.


4) Item Pipeline (pipelines.py) - Post processing of data to clean and make it readable. Also we can use this script to store the data in database. I have dumped all the data into a text file. We can easily import that data into a database like mongoDB/postgresSQL or move it to the cloud. 

5) Being nice - Obey the websites robot.txt and decrease the download delay (time to wait before crawling consecutive pages) to avoid suspicion. 



PART 2 ----- SEARCH

* What is it?
Set of relevant articles are displayed according to tfidf ranking based on user's search query.

* tf-idf - term frequency times inverse document frequency. You can read more about it here (https://en.wikipedia.org/wiki/Tf-idf). Easy and reliable ranking methodology for information retrieval.

* search.py - search implementation,building index and rank (tfidf)

* categories.py - preprocessing data and data abstraction for search

* index.py - command line interface


