#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dragline.runner import main
from dragline.parser import HtmlParser
from dragline.http import Request, RequestError
import settings
from items import *
import os
import csv
from settings import get_ua
from datetime import datetime
from dateutil import parser as dparser
import re
from settings import DEFAULT_REQUEST_ARGS
from dragline.shell import view


class Spider:
    def __init__(self, *args, **kwargs):
        self.name = "1833_AmazonAsinReviews"
        self.start = "https://www.amazon.com/"
        self.allowed_domains = []
        self.headers = DEFAULT_REQUEST_ARGS["headers"]
    
    def parse(self, response):
        if len(response.text)<10000:
            raise RequestError('Invalid Response')
        with open(os.path.join(os.path.dirname(__file__),'need_to_scrape.csv')) as f:
            reader = list(csv.DictReader(f))
            # reader = ["B000MFNB5O"]
            for asins in reader:
                asin_id = asins.get('October_ASIN_List')
                asin_id = asin_id.strip() if asin_id else None

                # asin_id = asins
                urls = 'https://www.amazon.com/dp/'+ asin_id
                searchurl = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias=aps&field-keywords="+asin_id
                meta={'resultsurl':searchurl,
                        'input_asin':asin_id,
                        'retried' : 0,
                        }
                yield Request(urls,callback=self.parse_product,meta=meta)

    # def parse_results(self,response):
        #check previous commit from 20 sept 2017
    
    #https://www.amazon.com/Dorman-521-872-Control-Arm/dp/B00GJ1OP00/ref=sr_1_1?ie=UTF8&qid=1504621211&sr=8-1&keywords=+B00GJ1OP00
    def parse_product(self,response):
        response.meta['Referer'] = response.url
        meta = response.meta
        input_asin = meta.get('input_asin')

        if "Sorry! We couldn't" in response.text or response.status_code==404:
            # self.logger.warning("Page Not Found %s"%response.url)
            data = {}
            data['Asin']=response.meta['input_asin']
            data['Url']=response.url
            Missing(**data).save()

        elif 'captcha' in response.text.lower():
            # self.logger.warning("Captcha Page url is %s,length is %d"%(response.url,len(response.text)))
            headers = {}
            headers['User-Agent'] = get_ua()
            headers['Host'] = "www.amazon.com"
            headers['Referer'] = response.url
            if response.meta['retried'] <= settings.MAX_RETRY:
                response.meta['retried'] = response.meta['retried'] + 1

                meta = {
                        'resultsurl' :response.meta['resultsurl'],
                        'input_asin':response.meta['input_asin'],
                        "Referer":response.url,
                        "headers":headers,
                        "retried":response.meta['retried'],
                       }
                yield Request(response.url,callback=self.parse_product,headers=headers,meta=meta,dont_filter=True)
            else:
                self.logger.warning("Rejecting %s"%(response.url))

        elif response.status == 503:
            self.logger.warning("Blocked page url is %s,length is %d"%(response.url,len(response.text)))
            raise RequestError("Page Blocked")
        elif len(response.text)<10000:
            headers = {}
            headers['User-Agent'] = get_ua()
            headers['Host'] = "www.amazon.com"
            headers['Referer'] = response.meta['Referer']
            if response.meta['retried'] <= settings.MAX_RETRY:
                response.meta['retried'] = response.meta['retried'] + 1
                meta = {    
                          'resultsurl' :response.meta['resultsurl'],
                          'input_asin':input_asin,
                          "Referer":response.meta['Referer'],
                          "headers":headers,
                          "retried":response.meta['retried'],
                       }
                yield Request(response.url,callback=self.parse_product,headers=headers,meta=meta,dont_filter=True)
            else:
                self.logger.warning("Rejecting %s"%(response.url))
        else:

            parser = HtmlParser(response)
            namepath = './/h1[@id="title"]/span[@id="productTitle"]/text()'
            brandpath1 = './/th[contains(text(),"Brand")]/following-sibling::td/text()'
            brandpath2 = './/table//td[contains(text(),"Brand")]/following-sibling::td/text()'
            brandpath3 = './/li[contains(b/text(),"Brand")]/text()'
            brandpath4 = './/a[@id="bylineInfo"]/text()'
            pricepath1 = './/span[@id="priceblock_dealprice"]/text()'
            pricepath2 = './/span[@id="priceblock_ourprice"]/text()'
            pricepath3 = './/span[@id="priceblock_saleprice"]/text()'
            pricepath4 = './/span[@class="a-color-price"]/text()'
            partnumberpath1 = './/th[contains(text(),"Part Number")]/following-sibling::td/text()'
            partnumberpath2 = './/table//td[contains(text(),"Part Number")]/following-sibling::td/text()'
            partnumberpath3 = './/th[contains(text(),"Item model number")]/following-sibling::td/text()'
            partnumberpath4 = './/li[contains(b/text(),"Item model number")]/text()'
            partnumberpath5 = './/li[contains(b/text(),"Part Number")]/text()'
            partnumberpath6 = './/li[contains(b/text(),"Model")]/text()'
            partnumberpath7 = './/th[contains(text(),"Model")]/following-sibling::td/text()'
            partnumberpath8 = './/table//td[contains(text(),"Model")]/following-sibling::td/text()'
            packagedimensionpath1 = './/th[contains(text(),"Package Dimension")]/following-sibling::td/text()'
            packagedimensionpath2 = './/table//td[contains(text(),"Package Dimension")]/following-sibling::td/text()'
            packagedimensionpath3 = './/li[contains(b/text(),"Package Dimension")]/text()'
            packagedimensionpath4 = './/li//span[contains(text(),"Package Dimension")]/following-sibling::span/text()'
            packagedimensionpath5 = './/th[contains(span/text(),"Package Dimension")]/following-sibling::td[1]//text()'
            asinpath1 = './/input[@id="ASIN"]/@value'
            asinpath2 = './/li[contains(b/text(),"ASIN")]/text()'
            asinpath3 = './/th[contains(text(),"ASIN")]/following-sibling::td/text()'
            #ratingpath = './/div[@id="revFMSR"]//span[contains(text(),"out of 5 stars")]/text()'
            ratingpath1 = './/div[@id="averageCustomerReviews"]//span[contains(@class,"reviewCount")][contains(@title,"out of 5 stars")]/@title'
            ratingpath2 = './/th[contains(text(),"Customer Reviews")]/following-sibling::td/text()'
            oempath1 = './/th[contains(text(),"OEM Part Number")]/following-sibling::td/text()'
            oempath2 = './/table//td[contains(text(),"OEM Part Number")]/following-sibling::td/text()'
            oempath3 = './/li[contains(b/text(),"OEM Part Number")]/text()'
            oempath4 = './/table//tr[contains(th//a/text(),"OEM Part Number")]/td/text()'
            oempath5 = './/table//tr[contains(td//a/text(),"OEM Part Number")]/td/text()'
            
            
            
            name = parser.xpath(namepath)
            if name:
                name = name[0].strip()
            else:
                #retry if no name       
                self.logger.warning("Bad output ( parse_reviews ).. Url is %s"%(response.url))
                raise RequestError('Invalid Page Response')    
            brand1 = parser.xpath(brandpath1)
            brand2 = parser.xpath(brandpath2)
            brand3 = parser.xpath(brandpath3)
            brand4 = parser.xpath(brandpath4)
            brand = brand1 if brand1 else brand2
            brand = brand3 if not brand else brand 
            brand = brand4 if not brand else brand       
            brand = brand[0].strip() if brand else None

            price1 = parser.xpath(pricepath1)
            price2 = parser.xpath(pricepath2)
            price3 = parser.xpath(pricepath3)
            price4 = parser.xpath(pricepath4)
            price = price1 if price1 else price2
            price = price3 if not price else price
            price = price4 if not price else price
            price = price[0].strip() if price else None
            # price = response.meta["price"] if not price else price

            partnumber1 = parser.xpath(partnumberpath1)
            partnumber2 = parser.xpath(partnumberpath2)
            partnumber3 = parser.xpath(partnumberpath3)
            partnumber4 = parser.xpath(partnumberpath4)
            partnumber5 = parser.xpath(partnumberpath5)
            partnumber6 = parser.xpath(partnumberpath6)
            partnumber7 = parser.xpath(partnumberpath7)
            partnumber8 = parser.xpath(partnumberpath8)
            partnumber = partnumber1 if partnumber1 else partnumber2
            partnumber = partnumber3 if not partnumber else partnumber
            partnumber = partnumber4 if not partnumber else partnumber
            partnumber = partnumber5 if not partnumber else partnumber
            partnumber = partnumber6 if not partnumber else partnumber
            partnumber = partnumber7 if not partnumber else partnumber
            partnumber = partnumber8 if not partnumber else partnumber
            partnumber = partnumber[0].strip() if partnumber else None

            packagedimension1 = parser.xpath(packagedimensionpath1)
            packagedimension2 = parser.xpath(packagedimensionpath2)
            packagedimension3 = parser.xpath(packagedimensionpath3)
            packagedimension4 = parser.xpath(packagedimensionpath4)
            packagedimension5 = parser.xpath(packagedimensionpath5)
            packagedimensiontext = packagedimension1 if packagedimension1 else packagedimension2 if packagedimension2 else packagedimension3 if packagedimension3 else packagedimension4 if packagedimension4 else packagedimension5
            packagedimension = ''.join([i.strip() for i in packagedimensiontext if i.strip()])
            packagedimension = packagedimension.strip() if packagedimension else None

            asin1 = parser.xpath(asinpath1)
            asin2 = parser.xpath(asinpath2)
            asin = asin1 if asin1 else asin2
            asin = asin[0].strip()
            
            rating1 = parser.xpath(ratingpath1)
            rating2 = parser.xpath(ratingpath2)
            if rating1:
                rating = rating1[0].replace('out of 5 stars','').strip()
            elif rating2:
                rating = ' '.join(''.join(rating2).split()).replace('out of 5 stars','').strip()
            else:
                rating = None

            oem1 = parser.xpath(oempath1)
            oem2 = parser.xpath(oempath2)
            oem3 = parser.xpath(oempath3)
            oem4 = parser.xpath(oempath4)
            oem5 = parser.xpath(oempath5)
            oem = oem1 if oem1 else oem2
            oem = oem3 if not oem else oem
            oem = oem4 if not oem else oem
            oem = oem5 if not oem else oem
            oem = oem[0].strip() if oem else None

            seller_rank_list = []
            seller_rank_xpath = './/th[contains(text(),"Sellers Rank")]/following-sibling::td/span//span'
            seller_ranks = parser.xpath(seller_rank_xpath)
            if seller_ranks:
                for rank in seller_ranks:
                    seller_rank = rank.xpath('.//text()')
                    seller_rank = ' '.join(''.join(seller_rank).split()) if seller_rank else None
                    seller_rank = seller_rank.replace('(See top 100)','')
                    seller_rank_list.append(seller_rank)
            if not seller_rank_list:
                sell_t2 = parser.xpath('//li[@id="SalesRank"]')
                sell_t2 = sell_t2[0].extract_text() if sell_t2 else None
                sell_t2 = sell_t2.replace('(See Top 100 in Beauty & Personal Care)','').replace(' (See Top 100 in Sports & Outdoors)','').replace(' .zg_hrsr { margin: 0; padding: 0; list-style-type: none; } .zg_hrsr_item { margin: 0 0 0 10px; } .zg_hrsr_rank { display: inline-block; width: 80px; text-align: right; } ',' | ').replace('Amazon Best Sellers Rank: ','').split('| ') if sell_t2 else None
                seller_rank_list = sell_t2 if sell_t2 else None

            
            searched_asin = input_asin
            # resultsurl = response.meta["resultsurl"]
            resultsurl = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias=aps&field-keywords="+ input_asin

            item_package_quantity = parser.xpath('//div[contains(label//text(),"Item Package Quantity:")]//following-sibling::span')
            item_package_quantity = item_package_quantity[0].extract_text() if item_package_quantity else None

            # new fileds
            # ship_check = parser.xpath('//a[contains(@title,"See All Buying Options") or contains(text(),"See All Buying Options")]')
            ship_check = parser.xpath('//div[contains(@data-feature-name,"shipsFromSoldByInsideBuyBox") or contains(@id,"shipsFromSoldByInsideBuyBox_feature_div")]')
            raw_ship_info = parser.xpath('//div[@id="merchant-info"]')
            raw_ship_info2 = parser.xpath('//span[contains(@id,"merchant-info")]')
            raw_ship_info3 = parser.xpath('//div[contains(@id,"merchant-info")]')

            ship_info = raw_ship_info[0].extract_text() if raw_ship_info else None
            ship_info2 = raw_ship_info2[0].extract_text() if raw_ship_info2 else None
            ship_info3 = raw_ship_info3[0].extract_text() if raw_ship_info3 else None
            ship_info =  ship_info if ship_info else ship_info2
            ship_info = ship_info if ship_info else ship_info3

            # view(response)
            # if not ship_info and ship_check:
            #     ship_info = "Ships from and sold by Amazon.com.."

            raw_inventory =  parser.xpath('//div[@id="availability"]')
            inventory = raw_inventory[0].extract_text() if raw_inventory else None

            raw_item_description = parser.xpath('.//h1[@id="title"]/span[@id="productTitle"]')
            item_description = raw_item_description[0].extract_text() if raw_item_description else None

            raw_no_of_cust = parser.xpath('.//a[contains(@id,"acrCustomerReviewLink")]')  #second_parser
            raw_no_of_cust =raw_no_of_cust[0].extract_text() if raw_no_of_cust else None

            date_first_available = parser.xpath('//th[contains(text(),"Date First Available")]//following-sibling::td') #second_parser
            date_first_available = date_first_available[0].extract_text() if date_first_available else None

            item_weight = parser.xpath('//th[contains(text(),"Item Weight")]//following-sibling::td') #second_parser
            item_weight_t2 = parser.xpath('//b[contains(text(),"Item Weight") or contains(text(),"Shipping Weight:")]//following-sibling::text()')
            item_weight_t2 = ', '.join(item_weight_t2).replace('(','').replace(')','').strip().strip(', ') if item_weight_t2 else None
            item_weight = item_weight[0].extract_text() if item_weight else item_weight_t2

            pro_dimen = parser.xpath('//th[contains(text(),"Product Dimensions") or contains(text(),"Package Dimensions")]//following-sibling::td') #second parser
            pro_dimen = pro_dimen[0].extract_text() if pro_dimen else None

            pro_dimen_t2 = parser.xpath('//b[contains(text(),"Product Dimensions:") or contains(text(),"Package Dimensions")]//following-sibling::text()')
            pro_dimen_t2 = ', '.join(pro_dimen_t2).strip().strip(', ') if pro_dimen_t2 else None
            pro_dimen = pro_dimen if pro_dimen else pro_dimen_t2

            #------------------------------------------------- Second response --------------------------------------------

            second_response = response.text.split('Product information')
            second_parser = second_response[1] if second_response and len(second_response)>=2 else None    
            checkreviews_p2 = ''    
            if second_parser:
                second_parser = HtmlParser(second_parser)
                seller_rank_list_p2 = []
                seller_ranks_p2 = second_parser.xpath(seller_rank_xpath)
                if seller_ranks_p2:
                    for rank_p2 in seller_ranks_p2:
                        seller_rank_p2 = rank_p2.xpath('.//text()')
                        seller_rank_p2 = ' '.join(''.join(seller_rank_p2).split()) if seller_rank_p2 else None
                        seller_rank_p2 = seller_rank_p2.replace('(See top 100)','')
                        seller_rank_list_p2.append(seller_rank_p2)

                partnumber9 = second_parser.xpath(partnumberpath1) 
                partnumber10 = second_parser.xpath(partnumberpath2)
                partnumber11 = second_parser.xpath(partnumberpath3)
                partnumber13 = second_parser.xpath(partnumberpath4)
                partnumber15 = second_parser.xpath(partnumberpath5)
                partnumber16 = second_parser.xpath(partnumberpath6)
                partnumber17 = second_parser.xpath(partnumberpath7)
                partnumber18 = second_parser.xpath(partnumberpath8)
                partnumber_p2 = partnumber9 if partnumber9 else partnumber10
                partnumber_p2 = partnumber11 if not partnumber_p2 else partnumber_p2
                partnumber_p2 = partnumber13 if not partnumber_p2 else partnumber_p2
                partnumber_p2 = partnumber15 if not partnumber_p2 else partnumber_p2
                partnumber_p2 = partnumber16 if not partnumber_p2 else partnumber_p2
                partnumber_p2 = partnumber17 if not partnumber_p2 else partnumber_p2
                partnumber_p2 = partnumber8 if not partnumber_p2 else partnumber_p2
                partnumber_p2 = partnumber_p2[0].strip() if partnumber_p2 else None

                oem6 = second_parser.xpath(oempath1) #second parser
                oem7 = second_parser.xpath(oempath2)
                oem8 = second_parser.xpath(oempath3)
                oem9 = second_parser.xpath(oempath4)
                oem10 = second_parser.xpath(oempath5)
                oem_p2 = oem6 if oem6 else oem7
                oem_p2 = oem8 if not oem_p2 else oem_p2
                oem_p2 = oem9 if not oem_p2 else oem_p2
                oem_p2 = oem10 if not oem_p2 else oem_p2
                oem_p2 = oem_p2[0].strip() if oem_p2 else None


                raw_item_description2 = second_parser.xpath('.//h1[@id="title"]/span[@id="productTitle"]')
                item_description2 = raw_item_description2[0].extract_text() if raw_item_description2 else None

                raw_no_of_cust2 = second_parser.xpath('.//a[contains(@id,"acrCustomerReviewLink")]')  #second_parser
                raw_no_of_cust2 =raw_no_of_cust2[0].extract_text() if raw_no_of_cust2 else None

                date_first_available2 = second_parser.xpath('//th[contains(text(),"Date First Available")]//following-sibling::td') #second_parser
                date_first_available2 = date_first_available2[0].extract_text() if date_first_available2 else None

                item_weight2 = second_parser.xpath('//th[contains(text(),"Item Weight")]//following-sibling::td') #second_parser
                item_weight2 = item_weight2[0].extract_text() if item_weight2 else None

                pro_dimen2 = second_parser.xpath('//th[contains(text(),"Product Dimensions") or contains(text(),"Package Dimensions")]//following-sibling::td') #second parser
                pro_dimen2 = pro_dimen2[0].extract_text() if pro_dimen2 else None
                checkreviews_p2 = second_parser.xpath('.//div[@data-hook="top-customer-reviews-widget"]')
            else : 
                self.logger.warning("No second parser %s,length is %d"%(response.url,len(response.text)))      
                oem_p2 = None
                partnumber_p2 = None
                seller_rank_list_p2 = None
                item_description2 = None
                item_weight2 = None
                pro_dimen2 = None
                raw_no_of_cust2 = None
                date_first_available2 = None

            product = {"Brand":brand,
                       "Part_No":partnumber if partnumber else partnumber_p2,
                       "ASIN":asin,
                       "Rating_Numbers":rating,
                       "OE_NO":oem if oem else oem_p2,
                       "Price":price,
                       "Customer_Name":None,
                       "Commented_Date":None,
                       "Comments":None,
                       "Url":response.url,
                       "Name":name,
                       "Searched_ASIN":searched_asin,
                       "Results_Url":resultsurl,
                       "Best_Seller_Rank":seller_rank_list if seller_rank_list else seller_rank_list_p2,
                       "Review_Url": None,
                        "Item_Description" : item_description if item_description else item_description2,
                        "Item_Package_Quantity" : item_package_quantity,
                        "Inventory" : inventory,
                        "Ship_Info" : ship_info,
                        "Item_Weight" : item_weight if item_weight else item_weight2,
                        "Product_Dimensions" : pro_dimen if pro_dimen else pro_dimen2,
                        "Number_of_Customer_Reviews" : raw_no_of_cust if raw_no_of_cust else raw_no_of_cust2,
                        "Date_First_Available" : date_first_available if date_first_available else date_first_available2,


                       }

            checkreviews = parser.xpath('.//div[@data-hook="top-customer-reviews-widget"]')
            if not checkreviews_p2:
                checkreviews_p2 = None
            checkreviews = checkreviews if checkreviews else checkreviews_p2
            #if the product contain reviews generate 'sort by recent' review url and crawl that page else save the data with blank reviews
            if checkreviews or raw_no_of_cust:
                re_urls = 'https://www.amazon.com/dp/'+ asin
                reviewsurl = re_urls.replace('/dp/','/product-reviews/')+"?ie=UTF8&reviewerType=avp_only_reviews&sortBy=recent"
                yield Request(reviewsurl,callback="parse_reviews",meta=product)
            else:
                # rint "\n *************************************************************** DATA 2 ********************************************************************** \n"
                Product(**product).save()    
    
    #https://www.amazon.com/Dorman-521-872-Control-Arm/product-reviews/B00GJ1OP00/ref=sr_1_1?ie=UTF8&qid=1504621211&sr=8-1&keywords=+B00GJ1OP007&reviewerType=avp_only_reviews&sortBy=recent
    def parse_reviews(self,response):
        # if response.status == 503 or response.status == 403:
        #     self.logger.warning("Blocked page ( parse_reviews ) Url is %s,length is %d"%(response.url,len(response.text)))
        #     raise RequestError("Request Blocked")
        # if response.status != 200:
        #     self.logger.warning("Bad output ( parse_reviews ).. Url is %s"%(response.url))
        #     raise RequestError("Invalid Response") 
        if len(response.text)<10000:
            raise RequestError('Invalid Response')
        parser = HtmlParser(response)
        product = response.meta
        mainreviewpath = './/div[@data-hook="review"]'
        mainreviews = parser.xpath(mainreviewpath)
        if not mainreviews:
            self.logger.warning("Zero reviews( parse_reviews ).. Url is %s"%(response.url))
            Product(**product).save()
        for review in mainreviews:
            custnamepath = './/a[@data-hook="review-author"]/text()'
            datepath = './/span[@data-hook="review-date"]/text()'
            textpath = './/span[@data-hook="review-body"]//text()'
            
            custname = review.xpath(custnamepath)
            custname = custname[0].strip() if custname else None
            date = review.xpath(datepath)
            date = date[0].strip() if date else None
            reviewtext = review.xpath(textpath)
            reviewtext = ' '.join([i.strip() for i in reviewtext if i.strip()])
            product["Customer_Name"] = custname
            product["Commented_Date"] = date
            product["Comments"] = reviewtext
            product["Review_Url"] = response.url
            # rint "\n *************************************************************** DATA 1********************************************************************** \n"
            Product(**product).save()
            # rint "\n ******************************************************************************************************************************************** "
            # reak

if __name__ == '__main__':
    main(Spider(), settings)





