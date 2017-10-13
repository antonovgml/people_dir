from pyramid.view import view_config
import logging
from bson import ObjectId
from bson.json_util import dumps

log = logging.getLogger(__name__)

@view_config(route_name='home', renderer='people_dir:templates/mytemplate.jinja2')
def my_view(request):
    log.debug('Starting my_view')
    
    session = request.session
    if 'counter' in session:
        session['counter'] += 1
    else:
        session['counter'] = 0
    
    
    
    return {'project': 'people_dir'}


# renderer='people_dir:templates/people.jinja2'
@view_config(route_name='people', renderer='json')
def people_view(request):
    
    return dict(people = list(request.db['people'].find()))