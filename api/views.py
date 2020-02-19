import json
from aiohttp import web
import asyncio
from abc import ABCMeta, abstractmethod


class Api(web.View):
	
	def riaser(self, request):
		return web.HTTPMethodNotAllowed(
			method=request.method,
			allowed_methods=request.method,
			headers=None,
			reason=None,
			body=None,
			text=None,
			content_type=None
		)
	
	async def get(self):
		raise self.riaser()
	
	async def post(self):
		raise self.riaser()
	
	async def put(self):
		raise self.riaser()

	async def delete(self):
		raise self.riaser()


		
class BookView(Api):
	
	async def get(self):
		response_obj = { 'status' : 'hello!' }
		return web.Response(text=json.dumps(response_obj))

class Redirect405(Api ):
	"""docstring for ClassName"""
	# def __init__(self,  request, *args, **kwargs):
	# 	# super(Redirect405, self).__init__(request)
	# 	# # self.request = request
	# 	# # self.args = args
	# 	# # self.kwargs = kwargs
	# 	pass


		