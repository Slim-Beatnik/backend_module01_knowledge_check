from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow

cache = Cache(config={"CACHE_TYPE": "SimpleCache"})  # creating and instance of Cache

limiter = Limiter(key_func=get_remote_address)  # creating and instance of Limiter

ma = Marshmallow()
