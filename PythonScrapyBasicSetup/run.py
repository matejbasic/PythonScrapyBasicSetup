from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

import sys,os.path
sys.path.append('/spiders/')
from spiders.iptester import IPTesterSpider
from spiders.uatester import UATesterSpider

configure_logging()
# importing project settings for further usage
# mainly because of the middlewares
settings = get_project_settings()
runner = CrawlerRunner(settings)

# running spiders sequentially (non-distributed)
@defer.inlineCallbacks
def crawl():
	yield runner.crawl(IPTesterSpider)
	yield runner.crawl(UATesterSpider)
	reactor.stop()

crawl()
reactor.run() # block until the last call
