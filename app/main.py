import bottle
from bottle_jwt import (JWTProviderPlugin, jwt_auth_required)
from tinydb import TinyDB, Query
import time

user_db = TinyDB('users.json')
event_db = TinyDB('events.json')

app = bottle.Bottle()

server_secret = 'TEAMROCKET'

class AuthBackend(object):
    user = {'id': 1237832, 'username': 'ben', 'password': '123', 'data': {'sex': 'male', 'active': True}}

    def authenticate_user(self, username, password):
        """Authenticate User by username and password.

        Returns:
            A dict representing User Record or None.
        """
        if username == self.user['username'] and password == self.user['password']:
            return self.user
        return None

    def get_user(self, user_id):
        if user_id == self.user['id']:
            return {k: self.user[k] for k in self.user if k != 'password'}
        return None

provider_plugin = JWTProviderPlugin(
    keyword='jwt',
    auth_endpoint='/auth',
    backend=AuthBackend(),
    fields=('username', 'password'),
    secret=server_secret,
    ttl=30
)

app.install(provider_plugin)


@app.get('/')
@jwt_auth_required
def private_resource():
    return {"Auth": "True"}


@app.post('/create_user')
def create_user():
    user_query = Query()
    username = bottle.request.forms.get('email')
    print(username)
    password = bottle.request.forms.get('password')
    if len(user_db.search(user_query.username == username)) > 0:
        return {'Error': 'User already exists!'}
    else:
        user_db.insert({'id': time.gmtime(), 'username': username, 'password': password})
        return {'Result': 'Success'}


bottle.run(app=app, port=8080)