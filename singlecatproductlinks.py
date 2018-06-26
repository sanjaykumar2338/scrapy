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
from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector


HEADERS = {
    'X-MicrosoftAjax': 'Delta=true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
}
urls_csv = "/var/www/html/brickset_scraper/brickset_scraper/2001_KTM_PRODUCTS.csv"
start_urls_MAIN= []
my_file = open(urls_csv, "r")
reader = csv.reader(my_file)
for i, row in enumerate(reader):
    if i == 0:
        pass
    else:
        start_urls_MAIN.append(row[0])
for url in start_urls_MAIN:
    print url
class BrickSetSpider(scrapy.Spider):
    name = "brickset_scraper"
    
    allowed_domains = ["kiddicare.com"]
    
    custom_settings = {
        "DOWNLOAD_DELAY": 0
    }
    #f = open("/var/www/html/brickset_scraper/brickset_scraper/2001_KTM_PRODUCTS.csv")
    #start_urls = [url.strip() for url in f.readlines()]
    #print '***********************'
    #print start_urls
    #print '************************'
    def start_requests(self):
        urls_csv = "/var/www/html/brickset_scraper/brickset_scraper/singlecatlink.csv"
        start_urls_MAIN= []
        start_urls_MAIN2 = []
        my_file = open(urls_csv, "r")
        reader = csv.reader(my_file)
        for i, row in enumerate(reader):
            if i == 0:
                pass
            else:
                start_urls_MAIN.append(row[0])
                start_urls_MAIN2.append(row[1])
        for idx, url in enumerate(start_urls_MAIN):
            category=start_urls_MAIN2[idx]
            if url != "":
                yield scrapy.Request(url=url,meta={'category': category},callback=self.parse)
            #break
    url='http://www.kiddicare.com'

    def parse(self, response):
        
        hxs = HtmlXPathSelector(response)
        #catname = hxs.select('//span[@class="breadcrumbLocation"]/text()').extract_first()
        category=response.meta['category']
        SET_SELECTOR = '.products-list-item-container'
        selector = Selector(response)
        blog_titles = selector.xpath("//div[@class='item-name']")
        selections = []
        for data in response.css(SET_SELECTOR):
            #print '*********************'
            #print data
            #print '*********************'
            
            for x in data.xpath("//div[@class='item-name']"):
                href_a = "a ::attr(href)"
                hrefs = x.css(href_a).extract()
                
                for href in hrefs:
                    href2 = "http://www.kiddicare.com"+href
                        
                    print '*********************'
                    print href2
                    print category
                    print '*********************'
                    
                   
                    yield {
                        "Url": href2,
                        "category": category,
                    }
                    
                  
                  
        NEXT_PAGE_SELECTOR = '#pag_next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
              