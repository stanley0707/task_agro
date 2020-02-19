import aiohttp_cors
from aiohttp import web
from api import setup_routes
from aiohttp_middlewares import cors_middleware, error_middleware
from aiohttp_middlewares.cors import DEFAULT_ALLOW_HEADERS


# ecтанавливаем кор доступ по незащищенному соединению для тестирования
app = web.Application(
	middlewares=(
		cors_middleware(
			origins=("http://localhost:8081", "http://localhost:8080"),
			allow_credentials=True),

		error_middleware(),
	)
)

setup_routes(app, web)
web.run_app(app)