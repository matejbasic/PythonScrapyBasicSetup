# -*- coding: utf-8 -*-
# just for ip address testing purposes

import logging
import scrapy
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
        if ip_address:
            logging.info('IP ADDRESS = %s', ip_address)
        else:
            logging.info('IP ADDRESS NOT FOUND')
