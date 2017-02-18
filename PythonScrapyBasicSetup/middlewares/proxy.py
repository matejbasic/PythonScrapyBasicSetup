import urllib2
from bs4 import BeautifulSoup
from xml.dom import minidom
import random
from scrapy.utils.project import get_project_settings
import logging

import getpass
import stem
import stem.connection
from stem import Signal
from stem.control import Controller


class TorProxyMiddleware(object):

	def __init__(self, *args, **kwargs):
		self.import_settings()
		self.req_counter = 0

	def change_ip_addres(self):
		with Controller.from_port(port=self.control_port) as controller:
			controller.authenticate(self.password)
			controller.signal(Signal.NEWNYM)
			controller.close()

	def import_settings(self):
		settings = get_project_settings()
		self.control_port 	= settings['CONTROL_PORT']
		self.password	  	= settings['AUTH_PASSWORD']
		self.http_proxy	  	= settings['HTTP_PROXY']
		self.max_req_per_ip = settings['MAX_REQ_PER_IP']

	def process_request(self, request, spider):
		self.req_counter += 1
		if self.max_req_per_ip is not None and self.req_counter > self.max_req_per_ip:
			self.req_counter = 0
			self.change_ip_addres()

		request.meta['proxy'] = self.http_proxy
		logging.info('Using proxy: %s' % request.meta['proxy'])
		return None

class HttpProxyMiddleware(object):
	proxies = []

	def __init__(self, *args, **kwargs):
		self.query_proxies()

	def query_proxies(self):
		request = urllib2.urlopen('http://proxylist.hidemyass.com/search-1311281')
		if request.getcode() == 200:
			soup = BeautifulSoup(request, 'html.parser')
			# get the table with proxy addresses
			data_grid = soup.find('table', id='listable')

			max_proxies = 100
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
					max_proxies -= 1
					if max_proxies < 1:
						break
		request.close()

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
		item = random.choice(self.proxies)
		request.meta['proxy'] = item['protocol'] + '://' + item['address'] + ':' + item['port']
		logging.info('Using proxy: %s' % request.meta['proxy'])

	def remove_failed_proxy(self, request, spider):
		proxy = request.meta['proxy']
		logging.log(logging.DEBUG, 'Removing failed proxy...')
		try:
			i = 0;
			for el in self.proxies:
				if el['address'] in proxy:
					del self.proxies[i]
					proxies_num = len(self.proxies)
					logging.log(logging.DEBUG, 'Removed failed proxy <%s>, %d proxies left' % (proxy, proxies_num))
					if proxies_num == 0:
						self.query_proxies()
					return True
				i += 1
		except:
			logging.log(logging.ERROR, 'Error while removing failed proxy')
		return False

	def process_exception(self, request, exception, spider):
		if self.remove_failed_proxy(request, spider):
			return request
		return None


	def process_response(self, request, response, spider):
		# really brutal filter
		if response.status == 200:
			return response
		else:
			return request
