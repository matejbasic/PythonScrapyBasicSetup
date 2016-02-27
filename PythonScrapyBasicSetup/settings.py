# -*- coding: utf-8 -*-

BOT_NAME = 'PythonScrapyBasicSetup'

SPIDER_MODULES = ['PythonScrapyBasicSetup.spiders']
NEWSPIDER_MODULE = 'PythonScrapyBasicSetup.spiders'

# maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS=32

# delay for requests for the same website (default: 0)
#DOWNLOAD_DELAY=3
# download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# disable cookies
COOKIES_ENABLED=False

# downloader middlewares
DOWNLOADER_MIDDLEWARES = {
	'PythonScrapyBasicSetup.middlewares.RandomUserAgentMiddleware': 400,
    'PythonScrapyBasicSetup.middlewares.ProxyMiddleware': 410,
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None
}

