"""  run porject python manage.py
"""
import logging
import asyncio
import functools
from aiohttp import web
from aiohttp_middlewares import (cors_middleware, error_middleware)
from routes import setup_routes
from settings import(HOST, PORT, CLIENT_PORT, DEBUG)
from asyncio import coroutine



def force_sync(fn):
	def wrapper(*args, **kwargs):
	    return fn(*args, **kwargs)
	return wrapper

force = force_sync if __name__ == '__main__' else coroutine

@force
def run(wsgi=True):
	app = web.Application(
		middlewares=(
			cors_middleware(
				origins=("http://localhost:%s" % CLIENT_PORT, "http://localhost:%s" % PORT),
				allow_credentials=True
				),
			error_middleware(),
			)
		)
		
	setup_routes(app, web)

	if wsgi:
		return app
	
	web.run_app(app, host=HOST, port=PORT)


	
if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	print(f'Develop server seccesfuly started on {HOST}:{PORT}')
	run(wsgi=False)