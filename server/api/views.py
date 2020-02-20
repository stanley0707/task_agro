import json
import datetime
from aiohttp import web
import asyncio
from abc import ABCMeta, abstractmethod
from pony.orm.serialization import to_dict
from pony.orm import select, db_session, desc, commit
from pony.orm.core import TransactionIntegrityError, ObjectNotFound
from models.models import Book
from asyncio_extras import threadpool


class Api(web.View):
	
	def __init__(self, request, *args, **kwargs):
		super(Api, self).__init__(request)
		self.args = args # основные параметры фильтрации
		self.kwargs = kwargs
		self.part = 5 # пагинация кол-во записей на странице
		self.page = 1 # пагинация номер страницы
		self.marker = (self.part * self.page) - self.part
		self.status = 200
		self.response_text='успешно'
		
	def riaser(self):
		return web.HTTPMethodNotAllowed(
			method=self.request.method,
			allowed_methods=self.request.method,
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

class BaseApi(Api):
	
	def orderizer(self):
		try:
			self.order = self.order_params[self.request.rel_url.query['order_by']]
		except KeyError:
			pass
	
	def params_construct(self):
		for k, v in self.request.rel_url.query.items():
			print(k, v)
			self.select.append(self.select_params(k, v))

	
	def init_paginate(self):
		# елси параметры пагинации переданы в качестве аргументов
		# в реквест заменияем self.page, self.part с 1 и 1 на полученные
		# данные и удаляем их из массива. Если данные при просвоились,
		# удалились из массива request_data и его длина ровна 0, то значит
		# получен запрос на отображение всех записей без фильтрации
		try:
			self.page, self.part = int(self.request.rel_url.query['page']), int(self.request.rel_url.query['part'])
		except KeyError:
			pass
		except ValueError:
			pass
	
	def query(self, *args, **kwargs):
		return to_dict(
			obj for obj in self.model.select(
					*self.select
				).order_by(self.order)[self.marker: self.marker+self.part]
			)
	
	def serializer(self, *args, **kwargs):
		with db_session: return json.dumps(
					self.query(),
					ensure_ascii=False,
				)
	
	def write_method(self, msg):
		with db_session:
			try:
				self.model = self.model[self.data['id']]
				self.model.set(**self.data)
			except KeyError:
				self.model(**self.data)
			
			except ObjectNotFound:
				self.response_text = 'книга не найдена'
				self.status = 404
				return False 
			
			else:
				try:
					commit()
					self.response_text = msg
				
				except ValueError:
					self.response_text = 'отсутсвует обязательное поле данных'
					self.status = 409

				except TransactionIntegrityError:
					self.response_text = 'книга с таким названием уже существует'
					self.status = 400

	def get_method(self):
		self.init_paginate()
		self.orderizer()
		self.params_construct()

	def delete_method(self, msg):
		with db_session:
			if self.data['success_del']:
				try:
					self.model[self.data['id']].delete()
					self.response_text = msg
					return True
				except ObjectNotFound:
					self.response_text = 'книга не найдена'
					self.status = 404
					return False
		self.response_text = "вы действительно хотите удалить эту книгу"
		self.status = 428



class BookView(BaseApi):
	
	# словарь сортировка
	# можно добвать сортировку в обратном порядке по параметру API
	order_params =  {
		'id': lambda obj: desc(obj.id),
		'year': lambda obj: desc(obj.year)
		}

	def __init__(self,  request, *args, **kwargs):
		super(BookView, self).__init__(request)
		self.order = self.order_params['year'] 
		self.select = []# поумолчания сортировка по году издания
		self.model = Book # модель данных View 
		self.args = args
		self.kwargs = kwargs
	
	# основной массив параметров для поиска публикаций 
	def select_params(self, key, value):
		return {
			'id': lambda obj: int(obj.year) == int(value),
			'author': lambda obj: str(obj.author) == value,
			'name': lambda obj: str(obj.name) == value,
			'year': lambda obj: str(obj.year) == value
		}[key]
	
	async def get(self):
		async with threadpool():
			super().get_method()
			return web.json_response(
						self.serializer(),
						status=self.status
					)
	
	async def post(self):
		self.data = dict(await self.request.json())
		async with threadpool():
			super().write_method('Книга усппешно сохранена')
			return web.json_response(
						text=self.response_text,
						status=self.status
					)

	async def put(self):
		self.data = await self.request.json()
		async with threadpool():
			super().write_method('Книга усппешно изменена')
			return web.json_response(
						text=self.response_text,
						status=self.status
					)

	async def delete(self):
		self.data = await self.request.json()
		async with threadpool():
			super().delete_method('Книга усппешно удалена')
			return web.json_response(
						text=self.response_text,
						status=self.status
					)

class AutorView(Api):
	async def get(self):
		return web.Response(
			)


		