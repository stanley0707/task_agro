import datetime
from .model import BaseRedisData
import tldextract

class Link(BaseRedisData):
	
	model = 'links'

	def __init__(self, *args, **kwargs):
		super(Link, self).__init__()
		self.args = args
		self.kwarg = kwargs
	
	def domain_parse(self, url):
		info = tldextract.extract(url)
		return "{}{}".format(info.domain, '.'+info.suffix if bool(info.suffix) else info.suffix)
	
	def get_domain(self, *args, **kwargs):
		# возвращаем множество уникальных
		# занчений типированное в список.
		queryset = {
				self.domain_parse(v) for k, v in self.filter(*args, **kwargs).items()
			}
		if not bool(kwargs):
			return list(queryset)
		else:
			return list(queryset.by_date(**kwargs)) 

	def save_to_redis(self, data):
		for link in data:
			self.set(int(datetime.datetime.now().timestamp()), link)
