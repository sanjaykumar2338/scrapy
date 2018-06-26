import scrapy
from sys import exit
import re
import os.path
#import urllib2
import csv
import string
import time
import random
from twisted.internet import reactor

from scrapy.http import FormRequest
from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from random import randrange, uniform

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
    #f = open("/var/www/html/brickset_scraper/brickset_scraper/2001_KTM_PRODUCTS.csv")
    #start_urls = [url.strip() for url in f.readlines()]
    #print '***********************'
    #print start_urls
    #print '************************'
    def start_requests(self):
        urls_csv = "/var/www/html/brickset_scraper/brickset_scraper/doclist.csv"
        start_urls_MAIN = []
        start_urls_MAIN2 = []
        start_urls_MAIN3 = []
        my_file = open(urls_csv, "r")
        reader = csv.reader(my_file)
        for i, row in enumerate(reader):
            if i == 0:
                pass
            else:
                #start_urls_MAIN.append(row[0])
                start_urls_MAIN.append(row[0])
                start_urls_MAIN2.append(row[1])
                #start_urls_MAIN3.append(row[2])
        #print(start_urls_MAIN)
        
        #for url in start_urls_MAIN:
        for idx, url in enumerate(start_urls_MAIN2):
            name=start_urls_MAIN[idx]
            #address=start_urls_MAIN3[idx]
            if url != "":
                yield scrapy.Request(url=url,meta={'name': name},callback=self.parse)
                
          
        
    url='https://www.ifm.org/'
  
    def parse(self, response):
        detailinfo=[]
        
        print('**********************************name******************************')
        names=response.meta['name']
        name=names.split(',')
        #print(len(name))
        if len(name)==1:
           detailinfo.append(name)
        else:
            detailinfo.append(name[0])
            detailinfo.append(name[1])
        print('**********************************name******************************')
        
        print('**********************************perviousaddress******************************')
        perviousaddress=''
        detailinfo.append(perviousaddress)
        print('**********************************perviousaddress******************************')
        
        print('**********************************phonefax******************************')
        indexes=[]
        phones=response.xpath('//div[@class="contactInfo__item"]/text()').extract()
        stocks = [x.strip() for x in phones]
        for idx, val in enumerate(stocks):
           if val:
                indexes.append(idx)
        if indexes:
            if(len(indexes)>1):
                phonenumber=phones[indexes[0]]
                faxnumber=phones[indexes[1]]
            else:
                phonenumber=phones[indexes[0]]
                faxnumber=''
        else:
            phonenumber=''
            faxnumber=''
        detailinfo.append(phonenumber)
        detailinfo.append(faxnumber)
        print('**********************************phonefax******************************')
        
        print('**********************************email******************************')
        email=response.xpath('//div[@class="contactInfo__item"]/a/text()').extract_first()
        if email:
           email=email.strip()
        else:
            email=''
        detailinfo.append(email)
        print('**********************************email******************************')
        
        print('**********************************hrefs******************************')
        href_a = ".contactInfo__item:last-child a ::attr(href)"
        hrefs = response.css(href_a).extract_first()
        if hrefs:
           hrefs=hrefs
        else:
            hrefs=''
        detailinfo.append(hrefs)
        print('**********************************hrefs******************************')
        
        print('**********************************addressstart******************************')
        addressindex=[]
        '''
        for address in response.xpath('//div[@class="contactInfo"]'):
            address = address.xpath("//div[@class='contactInfo__address']/a[1]/text()").extract()
        print('***********************************add***************************')
        print(len(address))
       
        print('***********************************add***************************')
        '''
        lengthcontact=len(response.xpath('//div[@class="contactInfo"]'))
        print(lengthcontact)
        if lengthcontact==3:
            address=response.css('.contactInfo:nth-child(2) a:nth-child(1)::text').extract()
        if lengthcontact==2:
            address=response.css('.contactInfo:nth-child(2) a:nth-child(1)::text').extract()
        if lengthcontact==1:
            address=response.css('.contactInfo:nth-child(1) a:nth-child(1)::text').extract()
        #address=response.css('.contactInfo:nth-child(1) a:nth-child(1)::text').extract()
        print(address)
        #print(response.xpath('//div[@class="contactInfo"]/div[@class="contactInfo__item"]/span[1]/descendant-or-self::div[@class="contactInfo__address"]/text()').extract())
        for idx, val in enumerate(address):
            addressindex.append(idx)
            print(idx,val)
        lastindex=addressindex[-1]
        '''
        if(len(address)<=4):
            lastindex=addressindex[-1]
        if(len(address) >=6):
            lastindex=3
        if(len(address) == 5):
            lastindex=2
        '''
        print(lastindex)
        practiceinfo=address[addressindex[0]]
        print('***********************************practiceinfo***************************')
        print(practiceinfo)
        print('***********************************practiceinfo***************************')
        detailinfo.append(practiceinfo)
        try:
            addrinfo=address[addressindex[1]]
        except IndexError:
            addrinfo=''
        print('***********************************addrinfo***************************')
        print(addrinfo)
        print('***********************************addrinfo***************************')
        try:
            addr2info=address[addressindex[2]]
            perviousadd=addrinfo+addr2info
            print('***********************************perviousadd***************************')
            print(perviousadd)
            print('***********************************perviousadd***************************')
            detailinfo.append(perviousadd)
        except IndexError:
            perviousadd=addrinfo
        
        countryinfo=address[addressindex[lastindex]].split(',')
       
        print(countryinfo)
        practicelocation=practiceinfo+perviousadd
        print('***********************************practicelocation***************************')
        print(practicelocation)
        print('***********************************practicelocation***************************')
        
        print('***********************************add1***************************')
        print(countryinfo)
        print('***********************************add1***************************')
        
        print('*******************pcity*****************')
        city=countryinfo[0]
        detailinfo.append(city)
        print('*******************pcity*****************')
        if countryinfo[1]:
                division=countryinfo[1].split()
                count=len(division)
                print(count)
                if count == 2:
                    print('*******************state*****************')
                    state=division[0]
                    detailinfo.append(state)
                    print('*******************postcode*****************')
                    postcode=division[1]
                    detailinfo.append(postcode)
                else:
                    print('*******************state*****************')
                    state=division[0]
                    detailinfo.append(state)
                    print('*******************postcode*****************')
                    postcode =division[1]
                    detailinfo.append(postcode)
                    print('*******************country*****************')
                    country=division[2]
                    detailinfo.append(country)
                    
        print('**********************************addressend******************************')    
        
        #for practiceaddress in response.xpath('//div[@class="contactInfo__address"]'):
            #practiceaddress = practiceaddress.xpath("a[1]/text()").extract()    
        #practiceaddress = " ".join([" ".join(elem.split()) for elem in practiceaddress])
        #detailinfo.append(practiceaddress)
        aboutmypractice=response.xpath('//div[contains(@class,"pageSubSection--text")]//h4[contains(text(),"About My Practice")]/following-sibling::p[1]/text()').extract()
        patientexpect=response.xpath('//div[contains(@class,"pageSubSection--text")]//h4[contains(text(),"What Patients Can Expect")]/following-sibling::p[1]/text()').extract()
        graduateschool=response.xpath('//div[contains(@class,"pageSubSection--text")]//h4[contains(text(),"Graduate School Education")]/following-sibling::p[1]/text()').extract()
        profassoc=response.xpath('//div[contains(@class,"pageSubSection--text")]//h4[contains(text(),"Professional Associations")]/following-sibling::p[1]/text()').extract()
        langspoken=response.xpath('//div[contains(@class,"pageSubSection--text")]//h4[contains(text(),"Languages Spoken")]/following-sibling::ul[@class="list--bull list--cols"][1]/li/text()').extract()
        medspec=response.xpath('//div[contains(@class,"pageSubSection--text")]//h4[contains(text(),"Medical Specialties")]/following-sibling::ul[@class="list--bull list--cols"][1]/li/text()').extract()
        medcondition=response.xpath('//div[contains(@class,"pageSubSection--text")]//h4[contains(text(),"Medical Conditions")]/following-sibling::ul[@class="list--bull list--cols"][1]/li/text()').extract()
        practicinfomation=response.xpath('//ul[@class="list--plain"]/li/text()').extract()
        #print(practicinfomation)
        yield {
                "name":detailinfo[0],
                "type":detailinfo[1],
                "Practice Name":detailinfo[7],
                "address":detailinfo[8],
                "city":detailinfo[9],
                "state":detailinfo[10],
                "postcode":postcode,
                "country":'US',
                "Phone":detailinfo[3],
                "Practice Location":practicelocation,
                "Fax":detailinfo[4],
                "Email": detailinfo[5],
                "Website Link": detailinfo[6],  
                "Practice Information": practicinfomation,
                "About My Practice":aboutmypractice,
                "What Patients Can Expect":patientexpect,
                "Medical Specialties":medspec,
                "Medical Conditions":medcondition,
                "Languages Spoken":langspoken,
                "Graduate School of Education":graduateschool,
                "Professional Associations":profassoc
                
                
            }
        #for full_desc in full_descs:
            #href = full_desc.css("p").extract()
            
            #desc=response.css(DESC_SELECTOR).extract_first()
            #print full_desc
            #descrpition=response.xpath(' //div[contains(@class,"full-description")]/p/li[descendant-or-self::text()]').extract()
           
            #print descrpition
       