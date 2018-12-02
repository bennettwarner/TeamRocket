import bottle
from bottle_jwt import (JWTProviderPlugin, jwt_auth_required)
from tinydb import TinyDB, Query
import random
event_db = TinyDB('events.json')

app = bottle.Bottle()

server_secret = 'TEAMROCKET'

class AuthBackend(object):
    user = {'id': 1237832, 'username': 'test', 'password': '123', 'data': {'sex': 'male', 'active': True}}

    def authenticate_user(self, username, password):
        """Authenticate User by username and password.

        Returns:
            A dict representing User Record or None.
        """
        print('Login attempt from: {}:{}'.format(username, password))

        if username == self.user['username'] and password == self.user['password']:
            return self.user
        return None

    def get_user(self, user_id):
        """Retrieve User By ID.

        Returns:
            A dict representing User Record or None.
        """
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

app.install(provider_plugin)


@app.get('/authtest')
@jwt_auth_required
def private_resource():
    return {"Auth": "True"}


@app.post('/api/event/create')
#@jwt_auth_required
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

@app.get('/api/event/list')
def get_events():
    return str(event_db.all())


@app.route('/')
def server_static():
    return bottle.static_file('index.html', root='../html')
@app.route('/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='../html')
@app.route('/js/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='../html/js')


bottle.run(app=app, port=8080)