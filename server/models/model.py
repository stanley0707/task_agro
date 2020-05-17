"""  """
import redis
import json
import threading
import time
import settings
from collections.abc import MutableMapping

class QuerySet(MutableMapping):
	def __init__(self, data=()):
		self.mapping = {}
		self.update(data)
	
	def __getitem__(self, key):
		return self.mapping[key]
	
	def __delitem__(self, key):
		value = self[key]
		del self.mapping[key]
		self.pop(value, None)
	
	def __setitem__(self, key, value):
		self.mapping[key] = value

	def __iter__(self):
		return iter(self.mapping)
	
	def __len__(self):
		return len(self.mapping)
	
	def __repr__(self):
		return f"{type(self).__name__}({self.mapping})"

	def by_date(self, date_from:int, date_to:int):
		return {k:v for k, v in self.mapping.items() if date_from < int(k) < date_to}


class BaseRedisData():
	def __init__(self, *args, **kwargs):
		self.redis = redis.StrictRedis(
				host=settings.REDIS_URL,
				port=6379,
				db=0,
				password=None,
				socket_timeout=None,
				charset="utf-8",
				decode_responses=True
			)
		self._construct()
		self.args = args
		self.kwargs = kwargs
	
	def set(self, key, val):
		self.redis.hmset(self.model, {
				key: val
			})
		
	def get(self, key):
		return self.redis.hget(self.model, key)

	def all(self, *args, **kwargs):
		return self.redis.hgetall(self.model)

	def filter(self, *args, **kwargs):
		return QuerySet(
				self.redis.hgetall(self.model)
			)
	
	def delete(self, key):
		self.redis.hdel(self.model, key)
	
	def _construct(self, data={'0':'0'}):
		# инициализируем данные модели
		# при первом запуске если ключ отсутсвует
		if not len(self.redis.hgetall(self.model)):
			self.redis.hmset(self.model, data)

	def cleaner(self, *args, **kwargs):
		time.sleep(kwargs['countdown'])
		self.delete(kwargs['key'])

	def clean(self, key, countdown):
		# можно заюзать на случай временного хранения данных
		# self.clean(key, drop_countdown)
		timerThread = threading.Thread(
				target=self.cleaner,
				kwargs={'key': key, 'countdown': countdown}
			)
		timerThread.daemon = True
		timerThread.start()
		
