from aiohttp import web
from api import setup_routes


app = web.Application()
setup_routes(app, web)
web.run_app(app)

