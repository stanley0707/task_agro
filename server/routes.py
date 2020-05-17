# routes.py
import pathlib
from api.views import (
        get_domain, post_urls
    )


PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app, web):
    app.router.add_get('/api/visited_domains', get_domain)
    app.router.add_post('/api/visited_links', post_urls)
    setup_static_routes(app)

def setup_static_routes(app):
    app.router.add_static('/static/',
                          path=PROJECT_ROOT / 'static',
                          name='static')
