from .models import  Link

class RedisData:
	""" """
	def __init__(self, *args, **kwargs):
		self.links = Link()
		self.args = args
		self.kwargs = kwargs

redis_data = RedisData()