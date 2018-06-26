import scrapy
from sys import exit
import re
import os.path
import urllib2
import csv
import string
import time
from twisted.internet import reactor

from scrapy.http import FormRequest
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector


HEADERS = {
    'X-MicrosoftAjax': 'Delta=true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
}


urls_csv = "/var/www/html/Projects/brickset_scraper/brickset_scraper/2001.csv"
categories_csv = "/var/www/html/Projects/brickset_scraper/brickset_scraper/2001_KTM_CATEGORIES.csv"
products_csv = "/var/www/html/Projects/brickset_scraper/brickset_scraper/2001_KTM_PRODUCTS.csv"
start_urls_MAIN= []
my_file = open(urls_csv, "r")
reader = csv.reader(my_file)
for i, row in enumerate(reader):
    if i == 0:
        pass
    else:
        start_urls_MAIN.append(row[0])

#start_urls_MAIN = ['http://sparepartsfinder.ktm.com/Views/Shared/CatalogPages.aspx?articleId=b6ee9f60-4bad-e411-80c6-005056a6249b&engine=False&clr=True&CTG=540 SXC']

class BrickSetSpider(scrapy.Spider):
    name = "brickset_scraper"
    
    allowed_domains = ["sparepartsfinder.ktm.com"]
    #start_urls_MAIN= []
    
    custom_settings = {
        "DOWNLOAD_DELAY": 0
    }
    
    """
    my_file = open(urls_csv, "r")
    reader = csv.reader(my_file)
    for i, row in enumerate(reader):
        if i == 0:
            pass
        else:
            start_urls_MAIN.append(row[0])
    """
    
    
    #print start_urls_MAIN
    #exit()
    
    start_urls = [start_urls_MAIN[0]]
    
    s = "123123STRINGabcabc"

    def find_between(self, s, first):
        try:
            print "*****************HUUUUAAAAAAAAA*******************"
            print self
            print "*****************//HUUUUAAAAAAAAA*******************"
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            #print "*****************HUUUUAAAAAAAAA*******************"
            #print end
            #print "*****************//HUUUUAAAAAAAAA*******************"
            return s[start:end]
        except ValueError:
            return ""

	#print find_between( s, "123", "abc" )

    def parse(self, response):
        """
        start_urls_MAIN= []
        my_file = open(urls_csv, "r")
        reader = csv.reader(my_file)
        for i, row in enumerate(reader):
            if i == 0:
                pass
            else:
                start_urls_MAIN.append(row[0])
        """
    
        try:
            counter0 = response.meta['counter0']
            counter_MAIN = response.meta['counter_MAIN']
            #start_urls_MAIN = response.meta['start_urls_MAIN']
        except:
            counter0 = int(0)
            counter_MAIN = int(0)
            #start_urls_MAIN = start_urls_MAIN
        
        # Get parsed url
        URL = response.url
        
        # url without category
        URL = URL.split('&CTG=')[0]
        
        SET_SELECTOR = '.gridrow'
        
        new_ar = []
        URL_ar = []
        __EVENTTARGET_ar = []
        __EVENTARGUMENT_ar = []
        __VIEWSTATE_ar = []
        __EVENTVALIDATION_ar = []
        NAME_ar = []
        COUNTER_ar = []
        
        count_response = len(response.css(SET_SELECTOR))

        if int(counter0) < int(count_response):
            print "*****************FINALLY*******************" 
            print counter0       
            print "*****************FINALLY*******************" 
            counter = int(1)       
            for brickset in response.css(SET_SELECTOR):
                #if counter < int(44):
                NAME_SELECTOR = ".//td[3]/a/text()"
                NAME = brickset.xpath(NAME_SELECTOR).extract_first()
                NAME = re.sub('[^a-zA-Z0-9 \n\.]', '', NAME)
        
                NEXT_PAGE_SELECTOR = "td a ::attr(href)"
                next_page = brickset.css(NEXT_PAGE_SELECTOR).extract_first()
                next_page = next_page.split("__doPostBack(")[1][:-5][1:]
        
                if counter < int(2):
                    __VIEWSTATE_SELECTOR = '//input[@id="__VIEWSTATE"]/@value'
                    __VIEWSTATE = response.xpath(__VIEWSTATE_SELECTOR).extract_first()
        
                    __EVENTVALIDATION_SELECTOR = '//input[@id="__EVENTVALIDATION"]/@value'
                    __EVENTVALIDATION = response.xpath(__EVENTVALIDATION_SELECTOR).extract_first()
        
                __EVENTTARGET = next_page
                __EVENTARGUMENT = ""
                URL_ar.append(URL)
                __EVENTTARGET_ar.append(__EVENTTARGET)
                __EVENTARGUMENT_ar.append(__EVENTARGUMENT)
                __VIEWSTATE_ar.append(__VIEWSTATE)
                __EVENTVALIDATION_ar.append(__EVENTVALIDATION)
                NAME_ar.append(NAME)
                COUNTER_ar.append(int(counter))
        
                counter += int(1)

            for idx,x in enumerate(URL_ar):
                counter = COUNTER_ar[idx]
                URL = URL_ar[idx]
                __EVENTTARGET =__EVENTTARGET_ar[idx]
                __EVENTARGUMENT =__EVENTARGUMENT_ar[idx]
                __VIEWSTATE = __VIEWSTATE_ar[idx]
                __EVENTVALIDATION = __EVENTVALIDATION_ar[idx]
                NAME = NAME_ar[idx]
        
                #print "******"
                #print URL
                #print "******"
        
                if int(idx) == int(counter0):
                    print "*********************IDX***********************"
                    print idx
                    print __EVENTTARGET
                    print "*********************IDX***********************"
                    data = {'__EVENTTARGET': __EVENTTARGET, '__EVENTARGUMENT': __EVENTARGUMENT, '__VIEWSTATE': __VIEWSTATE, '__EVENTVALIDATION': __EVENTVALIDATION}
                    break
            
            yield FormRequest(URL, formdata = data, meta={'category': NAME, 'counter': counter0, 'URL_MAIN': URL, 'counter_MAIN': int(counter_MAIN), 'dont_cache': True}, callback = self.parse_page, dont_filter=True)
        else:
            print "**********************************INTERVAL**********************************"
            print int(counter_MAIN)
            print "**********************************INTERVAL**********************************"
            try:
                print "**********************************POST INTERVAL**********************************"
                print int(counter_MAIN) + int(1)
                print start_urls_MAIN[int(counter_MAIN) + int(1)]
                print "**********************************POST INTERVAL**********************************"
                yield FormRequest(start_urls_MAIN[int(counter_MAIN) + int(1)], meta={'counter0': int(0), 'counter_MAIN': int(counter_MAIN) + int(1)}, callback = self.parse, dont_filter=True)
            except:
                print "**********************************THE END**********************************"
            
    def parse_page(self, response):
        counter = response.meta['counter']
        URL_MAIN = response.meta['URL_MAIN']
        counter_MAIN = response.meta['counter_MAIN']
        #start_urls_MAIN = response.meta['start_urls_MAIN']
        if counter < 100000000000000000000:
            # Get parsed url
            URL = response.url
            print "****************URLC****************"
            print response.meta['category']
            print response.meta['counter']
            print response.meta['URL_MAIN']
            print "****************URLC****************"
            hxs = HtmlXPathSelector(response)
            STATE_LABEL = hxs.select('//span[@id="StateLabel"]/text()').extract_first()
        
            IMAGE = hxs.select('//img[@id="CatalogPageImage"]//@src').extract_first()
            IMAGE = re.sub(r'.*Images', 'Images', IMAGE)
            IMAGE = "http://sparepartsfinder.ktm.com/"+IMAGE
            CATEGORY = response.meta['category']
        
            SET_SELECTOR = '.gridrow'
            for brickset in response.css(SET_SELECTOR):

                PRODUCT_REFERENCE_CODE_SELECTOR = ".//td[2]/a/text()"
                PRODUCT_REFERENCE_CODE = brickset.xpath(PRODUCT_REFERENCE_CODE_SELECTOR).extract_first()
                NAME_SELECTOR = ".//td[3]/a/text()"
                NAME = brickset.xpath(NAME_SELECTOR).extract_first()
                PRODUCT_NUMBER_SELECTOR = ".//td[4]/a/text()"
                PRODUCT_NUMBER = brickset.xpath(PRODUCT_NUMBER_SELECTOR).extract_first()
                PRODUCT_POSITION_SELECTOR = ".//td[1]/a/text()"
                PRODUCT_POSITION = brickset.xpath(PRODUCT_POSITION_SELECTOR).extract_first()
            
                PRODUCT_POSITION = re.findall(r'\d+', PRODUCT_POSITION)
                PRODUCT_POSITION = str(PRODUCT_POSITION[0])
            
                __VIEWSTATE_SELECTOR = '//input[@id="__VIEWSTATE"]/@value'
                __VIEWSTATE = response.xpath(__VIEWSTATE_SELECTOR).extract_first()
            
                __EVENTVALIDATION_SELECTOR = '//input[@id="__EVENTVALIDATION"]/@value'
                __EVENTVALIDATION = response.xpath(__EVENTVALIDATION_SELECTOR).extract_first()
            
                SET_SELECTOR2 = '#hotspots a'
                for hotspots in response.css(SET_SELECTOR2):
                    PRODUCT_POSITION_MARK_SELECTOR0 = '"'+""+PRODUCT_POSITION+'"'
                    PRODUCT_POSITION_MARK_SELECTOR = '//input[@value='+PRODUCT_POSITION_MARK_SELECTOR0+']/@id'

                    PRODUCT_POSITION_MARK_SELECTOR1 = hotspots.xpath(PRODUCT_POSITION_MARK_SELECTOR).extract_first()
                    PRODUCT_POSITION_MARK1 = ""
                    PRODUCT_POSITION_MARK2 = ""
                    PRODUCT_POSITION_MARK_SELECTOR2 = ""
                    
                    try:
                        if hotspots.xpath(PRODUCT_POSITION_MARK_SELECTOR).extract()[1]:
                            PRODUCT_POSITION_MARK_SELECTOR2 = hotspots.xpath(PRODUCT_POSITION_MARK_SELECTOR).extract()[1]
                            if PRODUCT_POSITION_MARK_SELECTOR2:
                                PRODUCT_POSITION_MARK2 = re.findall(r'\d+', PRODUCT_POSITION_MARK_SELECTOR2)
                                PRODUCT_POSITION_MARK2 = PRODUCT_POSITION_MARK2[0]
                                PRODUCT_POSITION_MARKK2 = "#position"+PRODUCT_POSITION_MARK2+" ::attr(style)"
                                PRODUCT_POSITION_MARK2 = response.css(PRODUCT_POSITION_MARKK2).extract_first()
                                if PRODUCT_POSITION_MARK_SELECTOR1:
                                    PRODUCT_POSITION_MARK1 = re.findall(r'\d+', PRODUCT_POSITION_MARK_SELECTOR1)
                                    PRODUCT_POSITION_MARK1 = PRODUCT_POSITION_MARK1[0]
                                    PRODUCT_POSITION_MARKK1 = "#position"+PRODUCT_POSITION_MARK1+" ::attr(style)"
                                    PRODUCT_POSITION_MARK1 = response.css(PRODUCT_POSITION_MARKK1).extract_first()
                                    break
                    except Exception:
                        if PRODUCT_POSITION_MARK_SELECTOR1:
                            PRODUCT_POSITION_MARK1 = re.findall(r'\d+', PRODUCT_POSITION_MARK_SELECTOR1)
                            PRODUCT_POSITION_MARK1 = PRODUCT_POSITION_MARK1[0]
                            PRODUCT_POSITION_MARKK1 = "#position"+PRODUCT_POSITION_MARK1+" ::attr(style)"
                            PRODUCT_POSITION_MARK1 = response.css(PRODUCT_POSITION_MARKK1).extract_first()
                            break

                
                if PRODUCT_POSITION_MARK1:
                    PRODUCT_POSITION_MARK1 = str(PRODUCT_POSITION_MARK1)

                    r1 = re.compile('left:(.*?)px')
                    m1 = r1.search(PRODUCT_POSITION_MARK1)
                
                    r2 = re.compile('top:(.*?)px')
                    m2 = r2.search(str(PRODUCT_POSITION_MARK1))

                    CONTENT_BETWEEN1 = m1.group(1)
                    CONTENT_BETWEEN2 = m2.group(1)

                    new_text = re.sub(r'(?s)(left:)(.*?)(px)', "left:"+str(int(CONTENT_BETWEEN1) - 12)+"px", PRODUCT_POSITION_MARK1)
                    new_text = re.sub(r'(?s)(top:)(.*?)(px)', "top:"+str(int(CONTENT_BETWEEN2) - 12)+"px", new_text)
                    new_text = re.sub(r'\s+', '', new_text)

                    PRODUCT_POSITION_MARK1 = new_text
                
                if PRODUCT_POSITION_MARK2:    
                    
                    PRODUCT_POSITION_MARK2 = str(PRODUCT_POSITION_MARK2)

                    r1 = re.compile('left:(.*?)px')
                    m1 = r1.search(PRODUCT_POSITION_MARK2)
                
                    r2 = re.compile('top:(.*?)px')
                    m2 = r2.search(str(PRODUCT_POSITION_MARK2))

                    CONTENT_BETWEEN1 = m1.group(1)
                    CONTENT_BETWEEN2 = m2.group(1)

                    new_text = re.sub(r'(?s)(left:)(.*?)(px)', "left:"+str(int(CONTENT_BETWEEN1) - 12)+"px", PRODUCT_POSITION_MARK2)
                    new_text = re.sub(r'(?s)(top:)(.*?)(px)', "top:"+str(int(CONTENT_BETWEEN2) - 12)+"px", new_text)

                    PRODUCT_POSITION_MARK2 = new_text
                
                if PRODUCT_POSITION_MARK2:
                    if PRODUCT_POSITION_MARK1 == PRODUCT_POSITION_MARK2:
                        PRODUCT_POSITION_MARK = PRODUCT_POSITION_MARK1
                        yield {
                            "ID": "",
                            "Active (0/1)": "1",
                            "Name": NAME,
                            "category": CATEGORY,
                            "Price tax excluded or Price tax included": "",
                            "Tax rules ID": "",
                            "Wholesale price": "",
                            "On sale (0/1)": "",
                            "Discount amount": "",
                            "Discount percent": "",
                            "Discount from (yyyy-mm-dd)": "",
                            "Discount to (yyyy-mm-dd)": "",
                            "Reference #": "",
                            "Supplier reference #": "",
                            "Supplier": "",
                            "Manufacturer": "",
                            "EAN13": "",
                            "UPC": "",
                            "Ecotax": "",
                            "Width": "",
                            "Height": "",
                            "Depth": "",
                            "Weight": "",
                            "Quantity": "",
                            "Minimal quantity": "",
                            "Visibility": "",
                            "Additional shipping cost": "",
                            "Unity": "",
                            "Unit price": "",
                            "Short description": "",
                            "Description": "",
                            "Tags (x" : "",
                            "Meta Title": "",
                            "Meta keywords": "",
                            "Meta Description": "",
                            "URL rewritten": "",
                            "Text when in stock": "",
                            "Text when backorder allowed": "",
                            "Available for order (0 = No, 1 = Yes)": "",
                            "Product available date": "",
                            "Product creation date": "",
                            "Show price": "",
                            "Image URLs (x,y,z...)": IMAGE,
                            "Delete existing images": "",
                            "Feature": "",
                            "Available online only": "",
                            "Condition": "",
                            "Customizable": "",
                            "Uploadable files": "",
                            "Text fields": "",
                            "Action when out of stock": "",
                            "ID / Name of shop": "",
                            "Advanced Stock Management": "",
                            "Depends on stock": "",
                            "warehouse": "",
                            "Product Refcode": PRODUCT_REFERENCE_CODE,
                            "Product No": PRODUCT_NUMBER,
                            "Product Pos": PRODUCT_POSITION,
                            "Pzos Mark": PRODUCT_POSITION_MARK,
                        }
                    else:
                        PRODUCT_POSITION_MARK = PRODUCT_POSITION_MARK1
                        yield {
                            "ID": "",
                            "Active (0/1)": "1",
                            "Name": NAME,
                            "category": CATEGORY,
                            "Price tax excluded or Price tax included": "",
                            "Tax rules ID": "",
                            "Wholesale price": "",
                            "On sale (0/1)": "",
                            "Discount amount": "",
                            "Discount percent": "",
                            "Discount from (yyyy-mm-dd)": "",
                            "Discount to (yyyy-mm-dd)": "",
                            "Reference #": "",
                            "Supplier reference #": "",
                            "Supplier": "",
                            "Manufacturer": "",
                            "EAN13": "",
                            "UPC": "",
                            "Ecotax": "",
                            "Width": "",
                            "Height": "",
                            "Depth": "",
                            "Weight": "",
                            "Quantity": "",
                            "Minimal quantity": "",
                            "Visibility": "",
                            "Additional shipping cost": "",
                            "Unity": "",
                            "Unit price": "",
                            "Short description": "",
                            "Description": "",
                            "Tags (x" : "",
                            "Meta Title": "",
                            "Meta keywords": "",
                            "Meta Description": "",
                            "URL rewritten": "",
                            "Text when in stock": "",
                            "Text when backorder allowed": "",
                            "Available for order (0 = No, 1 = Yes)": "",
                            "Product available date": "",
                            "Product creation date": "",
                            "Show price": "",
                            "Image URLs (x,y,z...)": IMAGE,
                            "Delete existing images": "",
                            "Feature": "",
                            "Available online only": "",
                            "Condition": "",
                            "Customizable": "",
                            "Uploadable files": "",
                            "Text fields": "",
                            "Action when out of stock": "",
                            "ID / Name of shop": "",
                            "Advanced Stock Management": "",
                            "Depends on stock": "",
                            "warehouse": "",
                            "Product Refcode": PRODUCT_REFERENCE_CODE,
                            "Product No": PRODUCT_NUMBER,
                            "Product Pos": PRODUCT_POSITION,
                            "Pzos Mark": PRODUCT_POSITION_MARK,
                        }
                        PRODUCT_POSITION_MARK = PRODUCT_POSITION_MARK2
                        yield {
                            "ID": "",
                            "Active (0/1)": "1",
                            "Name": NAME,
                            "category": CATEGORY,
                            "Price tax excluded or Price tax included": "",
                            "Tax rules ID": "",
                            "Wholesale price": "",
                            "On sale (0/1)": "",
                            "Discount amount": "",
                            "Discount percent": "",
                            "Discount from (yyyy-mm-dd)": "",
                            "Discount to (yyyy-mm-dd)": "",
                            "Reference #": "",
                            "Supplier reference #": "",
                            "Supplier": "",
                            "Manufacturer": "",
                            "EAN13": "",
                            "UPC": "",
                            "Ecotax": "",
                            "Width": "",
                            "Height": "",
                            "Depth": "",
                            "Weight": "",
                            "Quantity": "",
                            "Minimal quantity": "",
                            "Visibility": "",
                            "Additional shipping cost": "",
                            "Unity": "",
                            "Unit price": "",
                            "Short description": "",
                            "Description": "",
                            "Tags (x" : "",
                            "Meta Title": "",
                            "Meta keywords": "",
                            "Meta Description": "",
                            "URL rewritten": "",
                            "Text when in stock": "",
                            "Text when backorder allowed": "",
                            "Available for order (0 = No, 1 = Yes)": "",
                            "Product available date": "",
                            "Product creation date": "",
                            "Show price": "",
                            "Image URLs (x,y,z...)": IMAGE,
                            "Delete existing images": "",
                            "Feature": "",
                            "Available online only": "",
                            "Condition": "",
                            "Customizable": "",
                            "Uploadable files": "",
                            "Text fields": "",
                            "Action when out of stock": "",
                            "ID / Name of shop": "",
                            "Advanced Stock Management": "",
                            "Depends on stock": "",
                            "warehouse": "",
                            "Product Refcode": PRODUCT_REFERENCE_CODE,
                            "Product No": PRODUCT_NUMBER,
                            "Product Pos": PRODUCT_POSITION,
                            "Pzos Mark": PRODUCT_POSITION_MARK,
                        }
                else:
                    PRODUCT_POSITION_MARK = PRODUCT_POSITION_MARK1+" "
                    yield {
                            "ID": "",
                            "Active (0/1)": "1",
                            "Name": NAME,
                            "category": CATEGORY,
                            "Price tax excluded or Price tax included": "",
                            "Tax rules ID": "",
                            "Wholesale price": "",
                            "On sale (0/1)": "",
                            "Discount amount": "",
                            "Discount percent": "",
                            "Discount from (yyyy-mm-dd)": "",
                            "Discount to (yyyy-mm-dd)": "",
                            "Reference #": "",
                            "Supplier reference #": "",
                            "Supplier": "",
                            "Manufacturer": "",
                            "EAN13": "",
                            "UPC": "",
                            "Ecotax": "",
                            "Width": "",
                            "Height": "",
                            "Depth": "",
                            "Weight": "",
                            "Quantity": "",
                            "Minimal quantity": "",
                            "Visibility": "",
                            "Additional shipping cost": "",
                            "Unity": "",
                            "Unit price": "",
                            "Short description": "",
                            "Description": "",
                            "Tags (x" : "",
                            "Meta Title": "",
                            "Meta keywords": "",
                            "Meta Description": "",
                            "URL rewritten": "",
                            "Text when in stock": "",
                            "Text when backorder allowed": "",
                            "Available for order (0 = No, 1 = Yes)": "",
                            "Product available date": "",
                            "Product creation date": "",
                            "Show price": "",
                            "Image URLs (x,y,z...)": IMAGE,
                            "Delete existing images": "",
                            "Feature": "",
                            "Available online only": "",
                            "Condition": "",
                            "Customizable": "",
                            "Uploadable files": "",
                            "Text fields": "",
                            "Action when out of stock": "",
                            "ID / Name of shop": "",
                            "Advanced Stock Management": "",
                            "Depends on stock": "",
                            "warehouse": "",
                            "Product Refcode": PRODUCT_REFERENCE_CODE,
                            "Product No": PRODUCT_NUMBER,
                            "Product Pos": PRODUCT_POSITION,
                            "Pzos Mark": PRODUCT_POSITION_MARK,
                        }
                
            
            yield FormRequest(URL_MAIN, meta={'counter0': int(counter) + int(1), 'counter_MAIN': int(counter_MAIN)}, callback = self.parse, dont_filter=True)
