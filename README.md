# Amazon-ASIN-Review-Scraper
Data Scraper designed in Python Programming language to scrape various data from the live Amazon website .  The Spider uses the Amazon ASIN stored in the Redis database to identify each product and then scrape through the same to obtain the required data like Price, Brand, Description, Quantity, Weight, Rating ,  Reviews, Comments , Availability and so on. 

The spider send request to all the pages and use the Xpath to retrieve the various required data from the HTML page . The data obtained is saved to necessary format like CSV ,  JSON etc. 

Technology Used : Python, Dragline Shell , Redis, HTML,  Xpath , Selenium


Data extrated json sample :

[
{
    "ASIN": "B002XIIICY",
    "Best_Seller_Rank": [
        "#1,754,019 in Automotive (See top 100)",
        "#1,069 in Automotive > Replacement Parts > Engines & Engine Parts > Engine Parts > Oil Drain Plugs"
    ],
    "Brand": "Dorman",
    "Commented_Date": "on August 8, 2016",
    "Comments": "Perfect fit",
    "Customer_Name": "Rachel S",
    "Date_First_Available": "October 10, 2007",
    "Inventory": "Only 3 left in stock (more on the way).",
    "Item_Description": "Dorman 095-143.1 AutoGrade Oil Drain Plug Gasket",
    "Item_Package_Quantity": null,
    "Item_Weight": "2.4 ounces",
    "Name": "Dorman 095-143.1 AutoGrade Oil Drain Plug Gasket",
    "Number_of_Customer_Reviews": "4 customer reviews",
    "OE_NO": "2152; 2161; 652906; 7125 3170271; 9043012027; E45Y6734A; J3170271; N0138128",
    "Part_No": "951431",
    "Price": "$2.91",
    "Product_Dimensions": "5.4 x 3 x 0.2 inches",
    "Rating_Numbers": "3.4",
    "Results_Url": "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias=aps&field-keywords=B002XIIICY",
    "Review_Url": "https://www.amazon.com/product-reviews/B002XIIICY?ie=UTF8&reviewerType=avp_only_reviews&sortBy=recent",
    "Searched_ASIN": "B002XIIICY",
    "Ship_Info": "Ships from and sold by Amazon.com.",
    "Url": "https://www.amazon.com/dp/B002XIIICY"
},
