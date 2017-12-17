# -*- coding: utf-8 -*-
# just for user agent testing purposes

import logging
import scrapy
from bs4 import BeautifulSoup

class UATesterSpider(scrapy.Spider):
    name = 'UAtester'
    allowed_domains = ['whatsmyuseragent.org']
    start_urls = (
        'http://whatsmyuseragent.org/',
    )

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        user_agent = soup.p.text
        if user_agent:
            logging.info('USER AGENT = %s', user_agent)
        else:
            logging.info('USER AGENT NOT FOUND')
