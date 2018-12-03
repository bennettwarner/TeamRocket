# Written by Bennett Warner - Last updated 12/3/2018
# Package Imports
import bottle
import random
from tinydb import TinyDB, Query
from bottle_jwt import (JWTProviderPlugin, jwt_auth_required)

event_db = TinyDB('events.json')
app = bottle.Bottle()
server_secret = 'TEAMROCKET'


#Auth Framework
class AuthBackend(object):
    user = {'id': 1237832, 'username': 'test', 'password': '123'}

    def authenticate_user(self, username, password):
        print('Login attempt from: {}:{}'.format(username, password))
        if username == self.user['username'] and password == self.user['password']:
            return self.user
        return None

    def get_user(self, user_id):
        if user_id == self.user['id']:
            return {k: self.user[k] for k in self.user if k != 'password'}
        return None

provider_plugin = JWTProviderPlugin(
    keyword='jwt',
    auth_endpoint='/api/auth',
    backend=AuthBackend(),
    fields=('username', 'password'),
    secret=server_secret,
    ttl=30
)

#Install JWT auth framework
app.install(provider_plugin)


#########################
#### Event API Endpoint
#########################
# Methods:
#/event/<eventID>
#/event/list
#/event/list/<username>
#/event/create
#event/delete/<eventID>

@app.get('/api/event/<id>')
@jwt_auth_required
def get_events(id):
    event = Query()
    return str(event_db.search(event.id == id))


@app.get('/api/event/list')
@jwt_auth_required
def get_events():
    return str(event_db.all())


@app.get('/api/event/list/<user>')
@jwt_auth_required
def get_events(user):
    event = Query()
    return str(event_db.search(event.user == user))


@app.post('/api/event/create')
@jwt_auth_required
def create_event():
    name = bottle.request.forms.get('name')
    game = bottle.request.forms.get('game')
    location = bottle.request.forms.get('location')
    time = bottle.request.forms.get('time')
    description = bottle.request.forms.get('description')
    required = bottle.request.forms.get('required')
    fee = bottle.request.forms.get('fee')
    event_db.insert({'id': random.randint(1,100000), 'user': 'test', 'name': name, 'game': game, 'location': location, 'time': time, 'description': description, 'required': required, 'fee': fee})
    return {'Success': 'Event Created'}


@app.route('/api/event/delete/<event_id>')
@jwt_auth_required
def delete(event_id):
    event = Query()
    find_event = event_db.search(event.id == int(event_id))
    if event_id=='' or len(find_event) == 0:
        return {'Error':'Invalid event id'}
    else:
        event_db.remove(event.id == int(event_id))
        return {'Success': 'Event Removed'}


    
############################################    
#### Static file hosting
############################################
@app.route('/')
def server_static():
    return bottle.static_file('index.html', root='../html')


@app.route('/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='../html')


@app.route('/js/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='../html/js')

#Run App
bottle.run(app=app, port=8080)
