# -*- coding: utf-8 -*-
# just for ip address testing purposes

import scrapy
import logging
from bs4 import BeautifulSoup

class IPTesterSpider(scrapy.Spider):
    name = 'IPtester'
    allowed_domains = ['icanhazip.com']
    start_urls = (
        'https://icanhazip.com',
    )

    def parse(self, response):
    	soup = BeautifulSoup(response.body, 'html.parser')
        ip_address = soup.get_text().rstrip('\n')
        if len(ip_address) > 0:
            logging.info('IP ADDRESS = %s' % ip_address)
        else:
            logging.info('IP ADDRESS NOT FOUND')
        pass
