import scrapy
from sys import exit
import re
import os.path
#import urllib2
import csv
import string
import time
import unicodedata
from twisted.internet import reactor

from scrapy.http import FormRequest
from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from bs4 import BeautifulSoup
from scrapy.selector import HtmlXPathSelector
from w3lib.html import remove_tags

HEADERS = {
    'X-MicrosoftAjax': 'Delta=true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
}

class BrickSetSpider(scrapy.Spider):
    name = "brickset_scraper"
    
    allowed_domains = ["ifm.org"]
    
    custom_settings = {
        "DOWNLOAD_DELAY": 0
    }
    
    #start_urls = ['https://www.ifm.org/find-a-practitioner/?country=US&city=&province=&state_us=&state_ca=&postal_code=&pos=&advanced_search=&ifm_certified=&practitioner-first-name=&practitioner-last-name=&insurance=&medicare=&online=&phone=&primary-degree=&languages=&pg=%s',% page for page in xrange(1,54)]
    #url='https://www.ifm.org/find-a-practitioner/?country=US&city=&province=&state_us=&state_ca=&postal_code=&pos=&advanced_search=&ifm_certified=&practitioner-first-name=&practitioner-last-name=&insurance=&medicare=&online=&phone=&primary-degree=&languages='
    start_urls = ['https://www.ifm.org/find-a-practitioner/?country=US&city=&province=&state_us=&state_ca=&postal_code=&pos=&advanced_search=&ifm_certified=&practitioner-first-name=&practitioner-last-name=&insurance=&medicare=&online=&phone=&primary-degree=&languages=&pg=%s.html' % page for page in range(1,86)]
    def parse(self, response):
       
        
        SET_SELECTOR = '.cardGrid__item'
        '''
        addressinfo=[]
        for address in response.xpath('//div[@class="contactInfo__item"]'):
                address = address.xpath('span/text()').extract()
                finaladdress = " ".join([" ".join(elem.split()) for elem in address])
                if finaladdress:
                    yield {
                        "address":finaladdress,
                        "url":response.url
                    }
            
        #print(addressinfo)
        
            
        '''
        for brickset in response.css(SET_SELECTOR):

            NAME_SELECTOR = 'h5 a ::text'
            HREF_SELECTOR='h5 a ::attr(href)'
            name=brickset.css(NAME_SELECTOR).extract_first()
            href=brickset.css(HREF_SELECTOR).extract_first()
            yield {
                "name":name,
                "href":href
            }
            
            
              
         
        #print(addressinfo)
        #print ("Value available at index 1 : ", addressinfo[1])
        #print ("Value available at index 0 : ", addressinfo[0])
        #print ("Value available at index 2 : ", addressinfo[2])
        #print ("Value available at index 3 : ", addressinfo[3])
        '''
        conatct=response.xpath('//div[@class="contactInfo__item"]/text()').extract()
            for cont in conatct:
                contactinfo=cont.strip()
                yield {
                    "phone":contactinfo
                }
       
        NEXT_PAGE_SELECTOR = '.paginationMenu__pages a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract()
        for page_urls in next_page:
            
            if next_page:
                yield scrapy.Request(
                    response.urljoin(page_urls),
                    callback=self.parse
            )
            '''   
            