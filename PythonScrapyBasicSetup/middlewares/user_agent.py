from scrapy.utils.project import get_project_settings
from xml.dom import minidom
import urllib2
import random

class RandomUserAgentMiddleware(object):
	settings = get_project_settings()

	def __init__(self, *args, **kwargs):
		# print 'RandomUserAgentMiddleware'
		xmldoc = minidom.parse(urllib2.urlopen('http://techpatterns.com/downloads/firefox/useragentswitcher.xml'))
		item_list = xmldoc.getElementsByTagName('useragent')

		user_agents = []
		for s in item_list:
			user_agents.append(s.attributes['useragent'].value)

		self.settings.set('USER_AGENT_LIST', user_agents)

	def process_request(self, request, spider):
		ua = random.choice(self.settings.get('USER_AGENT_LIST'))
		if ua:
			request.headers.setdefault('User-Agent', ua)
