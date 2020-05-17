import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = os.environ.get('DEBUG') == 'True'
PORT = os.environ.get('SERVER_PORT')
HOST = os.environ.get('SERVER_HOST')
CLIENT_PORT = os.environ.get('CLIENT_PORT')
CLIENT_HOST = os.environ.get('CLIENT_HOST')
REDIS_URL = os.environ.get('REDIS_URL')
