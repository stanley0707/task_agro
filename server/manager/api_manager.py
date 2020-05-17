import asyncio
import json
from .base import BaseManager
import sys
		

class ApiManager(BaseManager):
	
	def __init__(self, model, *args, **kwargs):
		self.request = None
		self.params = None
		self.method = None
		self.model = model()
		self.status = 404
		self.args = args
		self.kwargs = kwargs
		self.response = self.response_array()
	
	def response_array(self, msg="no"):
		return {'data': {"status": msg}} 

	def construct_response(self, *args, **kwargs):
		self.METHOD_DICT.get(self.method)(self)

	def visited_domains(self):
		try:
			self.response['data']['domains'] = self.model.get_domain(
						date_from=int(self.params['from']),
						date_to=int(self.params['to'])
					)
		except KeyError:
			self.response['data']['domains'] = self.model.get_domain()
		continue:
			self.response['data']['status'] = 'ok'
			self.status = 200

	def run(self, task):
		self.request.loop.create_task(task(self.params['links']))
		self.response['data']['status'] = 'ok'
		self.status = 200

	@asyncio.coroutine
	def body_json(self, loader=json.loads):
		body = yield from self.request.text()
		return loader(body)


	

	

