import random
import logging
import urllib2
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
from scrapy.utils.project import get_project_settings

class TorProxyMiddleware(object):

    def __init__(self):
        self.import_settings()
        self.req_counter = 0

    def change_ip_address(self):
        with Controller.from_port(port=self.control_port) as controller:
            controller.authenticate(self.password)
            controller.signal(Signal.NEWNYM)
            controller.close()

    def import_settings(self):
        settings = get_project_settings()
        self.password = settings['AUTH_PASSWORD']
        self.http_proxy = settings['HTTP_PROXY']
        self.control_port = settings['CONTROL_PORT']
        self.max_req_per_ip = settings['MAX_REQ_PER_IP']

        self.exit_nodes = settings['EXIT_NODES']
        if self.exit_nodes:
            with Controller.from_port(port=self.control_port) as controller:
                controller.authenticate(self.password)
                controller.set_conf('ExitNodes', self.exit_nodes)
                controller.close()

    def process_request(self, request, spider):
        self.req_counter += 1
        if self.max_req_per_ip is not None and self.req_counter > self.max_req_per_ip:
            self.req_counter = 0
            self.change_ip_address()

        request.meta['proxy'] = self.http_proxy
        logging.info('Using proxy: %s', request.meta['proxy'])
        return None

class HttpProxyMiddleware(object):
    proxies = []
    max_proxies = 100
    source = {
        'port': 8080,
        'type': 'HTTP',
        'url': 'https://www.proxydocker.com/search?port=%d&type=%s&anonymity=All&country=All&city=All'
    }

    def __init__(self):
        self.query_proxies()

    def _build_source_url(self):
        return self.source['url'] % (self.source['port'], self.source['type'])

    def query_proxies(self):
        request = urllib2.urlopen(self._build_source_url())
        if request.getcode() == 200:
            i = 0
            soup = BeautifulSoup(request, 'html.parser')
            for row in soup.find_all('tr'):
                cells = row.findAll('td')
                if len(cells) > 2:
                    self.proxies.append({
                        'address': cells[0].text.strip(),
                        'protocol': cells[1].text.lower().strip()
                    })
                    i += 1
                    if i == self.max_proxies:
                        break
        request.close()

    def process_request(self, request, spider):
        proxy = random.choice(self.proxies)
        request.meta['proxy'] = proxy['protocol'] + '://' + proxy['address']
        logging.info('Using proxy: %s', request.meta['proxy'])

    def remove_failed_proxy(self, request, spider):
        failed_proxy = request.meta['proxy']
        logging.log(logging.DEBUG, 'Removing failed proxy...')
        try:
            i = 0
            for proxy in self.proxies:
                if proxy['address'] in failed_proxy:
                    del self.proxies[i]
                    proxies_num = len(self.proxies)
                    logging.log(logging.DEBUG, \
                        'Removed failed proxy <%s>, %d proxies left', failed_proxy, proxies_num)
                    if proxies_num == 0:
                        self.query_proxies()
                    return True
                i += 1
        except KeyError:
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
        return request
