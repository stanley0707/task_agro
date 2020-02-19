import aiohttp_cors
from .views import BookView


def setup_routes(app, web):
    app.add_routes([
    		web.view('/api/books', BookView),
    	])