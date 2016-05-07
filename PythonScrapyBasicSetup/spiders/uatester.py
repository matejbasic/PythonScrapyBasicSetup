# -*- coding: utf-8 -*-
# just for user agent testing purposes

import scrapy
import logging
from bs4 import BeautifulSoup

class UATesterSpider(scrapy.Spider):
    name = 'UAtester'
    allowed_domains = ['useragentstring.com']
    start_urls = (
        'http://www.useragentstring.com/',
    )

    def parse(self, response):
    	soup = BeautifulSoup(response.body, 'html.parser')
        ua_container = soup.select('#uas_textfeld')[0].encode('UTF-8')
        ua = BeautifulSoup(ua_container, 'html.parser').get_text()
        logging.info("USER AGENT = %s" % ua)
        pass
