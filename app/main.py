import bottle
from bottle_jwt import (JWTProviderPlugin, jwt_auth_required)
from tinydb import TinyDB, Query

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


bottle.run(app=app, port=8080)