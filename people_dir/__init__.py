from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from urllib.parse import urlparse
from pymongo import MongoClient, uri_parser
from pyramid.renderers import JSON
from bson import ObjectId
import datetime
from textwrap import indent
from pprint import pprint

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    
    config.add_route('people', '/people')
    
    # Configure JSON rendering
    json_renderer = JSON(indent=4)
    json_renderer.add_adapter(ObjectId, lambda obj, request: str(obj))
    json_renderer.add_adapter(datetime.datetime, lambda obj, request: obj.isoformat())
    config.add_renderer('json', json_renderer)
    
        
    # Configure MongoDB
    
    mongo_uri = uri_parser.parse_uri(settings['mongo_uri'], default_port=27017, validate=True, warn=False)
    
    pprint(mongo_uri)
# {
#     'nodelist': <list of (host, port) tuples>,
#     'username': <username> or None,
#     'password': <password> or None,
#     'database': <database name> or None,
#     'collection': <collection name> or None,
#     'options': <dict of MongoDB URI options>
# }

    
#     mongo_db = settings['mongo_db']
#     mongo_admin = settings['mongo_admin']
#     mongo_password = settings['mongo_password']
    
    config.registry.db = MongoClient(settings['mongo_uri'])
    
    def add_db(request):
       db = config.registry.db[mongo_uri['database']]
       pprint(db)
#        if mongo_uri['username'] and mongo_uri['password']:
#            db.authenticate(mongo_uri['username'], mongo_uri['password'])
       return db
    
    config.add_request_method(add_db, 'db', reify=True)
    
    config.set_session_factory(SignedCookieSessionFactory('!#SecretPassword#!'))
    config.scan()
    return config.make_wsgi_app()
