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
from scrapy.selector import Selector


HEADERS = {
    'X-MicrosoftAjax': 'Delta=true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
}

class BrickSetSpider(scrapy.Spider):
    name = "brickset_scraper"
    
    allowed_domains = ["kiddicare.com"]
    
    custom_settings = {
        "DOWNLOAD_DELAY": 0
    }
    
    start_urls = ['http://www.kiddicare.com']
    url='http://www.kiddicare.com'

    def parse(self, response):
        SET_SELECTOR = '#menu'
        selector = Selector(response)
        blog_titles = selector.xpath("//ul[@id='menu']")
        selections = []
        for data in response.css(SET_SELECTOR):
            #print '*********************'
            #print data
            #print '*********************'
            
            for x in data.xpath('.//li'):
                href_a = ".dropdown_6columns li a ::attr(href)"
                hrefs = x.css(href_a).extract()
                for href in hrefs:
                    href2 = "http://www.kiddicare.com"+href
                    #print '*********************'
                    #print "http://www.kiddicare.com"+href
                    #print '*********************'
                    yield {
                        "Url": href2
                    }
                
