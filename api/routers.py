from .views import BookView

def setup_routes(app, web):
    app.add_routes([
    		web.view('/', BookView),
    	])