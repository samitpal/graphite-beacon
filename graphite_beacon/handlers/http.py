import urllib
import json

from tornado import gen, httpclient as hc
from graphite_beacon.handlers import AbstractHandler, LOGGER


class HttpHandler(AbstractHandler):

    name = 'http'

    # Default options
    defaults = {
        'method': 'GET',
    }

    def init_handler(self):
        self.url = self.options.get('url')
        assert self.url, 'URL is not defined'
        self.method = self.options['method']
        self.client = hc.AsyncHTTPClient()

    @gen.coroutine
    def notify(self, service, level, alert, value, target=None, ntype=None, rule=None):
        LOGGER.debug("Handler (%s) %s", self.name, level)

        message = self.get_short(service, level, alert, value, target=target, ntype=ntype, rule=rule)
        data = {'service': service, 'alert': alert.name, 'desc': message, 'severity': level}
        if target:
            data['target'] = target
        if rule:
            data['rule'] = rule['raw']

        if alert.source == 'graphite':
            data['value'] = str(value)
	# alertmanager format
	data = [{'labels': data}]
	body = json.dumps(data)
 	#LOGGER.debug(body)
        yield self.client.fetch(self.url, method=self.method, body=body)
