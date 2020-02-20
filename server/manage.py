"""  run porject python manage.py
"""
import asyncio
from aiohttp import web
from aiohttp_wsgi import WSGIHandler
from aiohttp_middlewares import (
		cors_middleware, error_middleware
		)
from api import setup_routes
from settings import(
		HOST, PORT, CLIENT_PORT, DEBUG
	)

# ecтанавливаем кор доступ по незащищенному соединению для тестирования
def run():
	app = web.Application(middlewares=(
					cors_middleware(origins=(
						"http://localhost:%s" % CLIENT_PORT, "http://localhost:%s" % PORT),
						allow_credentials=True
					), error_middleware(),
				))
	wsgi_handler = WSGIHandler(app)
	setup_routes(app, web)
	web.run_app(app, host=HOST, port=PORT)

if __name__ == '__main__':
	run()