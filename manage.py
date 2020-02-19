from aiohttp import web
from api import setup_routes


app = web.Application()
setup_routes(app, web)
web.run_app(app, host='127.0.0.1', port=8080)