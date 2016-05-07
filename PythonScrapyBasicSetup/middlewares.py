import os
import random
import re
import base64
from scrapy.utils.project import get_project_settings
from bs4 import BeautifulSoup
from xml.dom import minidom
import urllib2
import logging

class ProxyMiddleware(object):

	proxies = []

	def __init__(self, *args, **kwargs):
		fin = urllib2.urlopen('http://proxylist.hidemyass.com/search-1311281')
		soup = BeautifulSoup(fin, 'html.parser')
		# get the table with proxy addresses 
		data_grid = soup.find('table', id='listable')
		# iterate through the rows
		for tr in data_grid.tbody.findAll('tr'):
			i = 0
			item = {}
			for td in tr.findAll('td'):
				if i == 1: # ip address
					item['address'] = self.get_ip(td)
				elif i == 2:
					item['port'] = td.get_text().strip()
				elif i == 6:
					item['protocol'] = td.get_text().lower().strip() 	
				i += 1
			# if everything is scraped/defined, save to proxies list
			if 'ip_address' and 'port' and 'protocol' in item:
				self.proxies.append(item)

		fin.close()

	def get_ip(self, td):
		# getting ip address is a little bit tricky but this solution 
		# is simple and fast, for more info check 
		# https://blueshellgroup.wordpress.com/2013/04/15/creating-a-private-database-of-proxies-part-2/
		span = td.find('span')
		styles = str(span.find('style')).split('.')
		for k in range(1, len(styles)):
			style = styles[k].split('{')
			if 'none' in style[1]:
				[s.extract() for s in span('span', { 'class' : style[0] })]

		[s.extract() for s in span('style')]
		[s.extract() for s in span(['span', 'div'], style='display:none')]

		return span.get_text().replace('\n', '').replace('\t', '').strip()

	@classmethod
	def from_crawler(cls, crawler):
		settings = get_project_settings()
		return cls(crawler.settings)

	def process_request(self, request, spider):
		# don't overwrite with a random one
		if 'proxy' in request.meta:
			return
		
		item = random.choice(self.proxies)
		request.meta['proxy'] = item['protocol'] + '://' + item['address'] + ':' + item['port']
		#print request.meta['proxy']

	def process_exception(self, request, exception, spider):
		proxy = request.meta['proxy']
		print('Removing failed proxy <%s>, %d proxies left' % (proxy, len(self.proxies)))
		try:
			i = 0;
			for el in self.proxies:
				if el['address'] == proxy:
					del self.proxies[i]
					break
				i += 1
		except ValueError:
			pass

class RandomUserAgentMiddleware(object):

	settings = get_project_settings()

	def __init__(self, *args, **kwargs):
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

