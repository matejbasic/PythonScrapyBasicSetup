import random
from xml.dom import minidom
from scrapy.utils.project import get_project_settings

class RandomUserAgentMiddleware(object):
    settings = get_project_settings()
    source_path = 'data/user_agents.xml'

    def __init__(self, *args, **kwargs):
        xmldoc = minidom.parse(self.source_path)
        items = xmldoc.getElementsByTagName('useragent')
        user_agents = [item.attributes['value'].value for item in items]

        self.settings.set('USER_AGENT_LIST', user_agents)

    def process_request(self, request, spider):
        user_agent = random.choice(self.settings.get('USER_AGENT_LIST'))
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)
