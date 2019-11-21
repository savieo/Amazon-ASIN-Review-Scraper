# Amazon-ASIN-Review-Scraper
Data Scraper designed in Python Programming language to scrape various data from the live Amazon website .  The Spider uses the Amazon ASIN stored in the Redis database to identify each product and then scrape through the same to obtain the required data like Price, Brand, Description, Quantity, Weight, Rating ,  Reviews, Comments , Availability and so on. 

The spider send request to all the pages and uses the Xpath to retrieve the various required data from the HTML page . The data obtained is saved to necessary format like CSV ,  JSON etc. 

Technology Used : Python, Dragline Shell , Redis, HTML,  Xpath , Selenium
