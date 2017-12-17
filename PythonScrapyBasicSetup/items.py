# -*- coding: utf-8 -*-

import scrapy

class ProxyItem(scrapy.Item):
    protocol = scrapy.Field()
    address = scrapy.Field()
    port = scrapy.Field()
