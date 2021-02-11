#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: saul
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 20:33:27 2018

@author: saul
"""

from urllib.parse import urlparse
import scrapy 

from scrapy.http import Request
from scrapy.http import TextResponse
from scrapy.selector import Selector
from scrapy import *
import subprocess

import PyPDF2
from PyPDF2 import PdfFileReader, utils
#import textract

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class pwc(scrapy.Spider):
    name = "royal"

    allowed_domains = ["financialservices.royalcommission.gov.au",]
    #start_urls = ["http://www.pwc.com/us/en/tax-services/publications/research-and-insights.html"]
    start_urls = ["https://financialservices.royalcommission.gov.au/pages/results.aspx?k=munich re"]

    def parse(self, response):
        #subprocess.call(["rm output.csv","/home/saul/asic/asic/spiders"])
        
        query = '//div[@class="srch-Title3"]/a/@href'
        urls = response.xpath(query).extract()
        #print ("URLLLL :", urls)
        for url in urls:
            absolute_url = response.urljoin(url)
            #yield Request(absolute_url,
                   #self.parse_article) # recursively calls parse_article at each href containing pdf
            #print ("Absolute_URLLLL :", absolute_url)
            yield scrapy.Request(absolute_url, self.save_pdf) # Send PDF link to download
            #print ("SECOND RUN   :\n",)
            filename = absolute_url.split('/')[-1] #PDF file name
            #print("FILE NAME      :\n", filename)
            #self.logger.info('Saving PDF %s', filename )
            #with open(filename , 'wb') as f:
                #f.write(response.body) 
            #f.close()
            #yield from self.readPDF(filename)
            

    def save_pdf(self, response):
        path = response.url.split('/')[-1] #File name
        print("PATH :",path)
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body) 
        yield from self.readPDF(path)
        #yield from self.send_request(self, param)
    
    def readPDF(self, PDFfilename):
        pdfdetails = {}
        print("READINNG PDF FILE :", PDFfilename)
        pdfReader = PyPDF2.PdfFileReader(open(PDFfilename, "rb")) #PdfFileReader object
        
        print("PDF Reader :", pdfReader.numPages)
        
        pdfdetails[PDFfilename] = pdfReader.numPages
        
        print(pdfdetails)
        
        num_pages = pdfReader.numPages
        count = 0
        text = ""
        keyword = stopwords.words('Munich re')
        #The while loop will read each page
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count +=1
            text += pageObj.extractText()
            tokens = word_tokenize(text)
            for word in pageObj.extractText():
                if word in keyword:
                    print("Page Number : ",count)
                
        
        print("TEXT ", text)
