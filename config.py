import os

DEBUG = True
ROOT = os.path.abspath(os.path.dirname(__file__))

PORT = 8080
WEB_URL = 'http://localhost'

PG_DSN = 'postgresql://postgres:qwerty@127.0.0.1:5432/comments'
PG_POOL_SIZE = 10

COMMENTS_ON_PAGE = 100
