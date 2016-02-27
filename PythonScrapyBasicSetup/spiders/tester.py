# -*- coding: utf-8 -*-
# just for testing purposes

import scrapy
import logging
from bs4 import BeautifulSoup

class TesterSpider(scrapy.Spider):
    name = "tester"
    allowed_domains = ["whatismyipaddress.com"]
    start_urls = (
        'http://www.whatismyipaddress.com/',
    )

    def parse(self, response):
    	soup = BeautifulSoup(response.body, 'html.parser')

        ip_container = soup.select('#section_left > div:nth-of-type(2) > a:nth-of-type(1)')[0].encode("UTF-8")
        ip = BeautifulSoup(ip_container, 'html.parser').get_text()
        logging.info("IP ADDRESS = %s" % ip)
        pass
