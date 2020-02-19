from .views import BookView, Api, Redirect405

def setup_routes(app, web):
    app.add_routes([
    		web.view('/', BookView),
    	])