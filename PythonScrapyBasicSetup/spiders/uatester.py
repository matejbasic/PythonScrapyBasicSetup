# -*- coding: utf-8 -*-
# just for user agent testing purposes

import scrapy
import logging
from bs4 import BeautifulSoup

class UATesterSpider(scrapy.Spider):
    name = 'UAtester'
    allowed_domains = ['whatsmyuseragent.org']
    start_urls = (
        'http://whatsmyuseragent.org/',
    )

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        ua = soup.p.text
        logging.info('USER AGENT = %s' % ua)
        pass
