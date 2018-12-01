import bottle
from bottle_jwt import (JWTProviderPlugin, jwt_auth_required)
from tinydb import TinyDB, Query


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
        """Retrieve User By ID.

        Returns:
            A dict representing User Record or None.
        """
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
    return {"scope": "For your eyes only!", "user": bottle.request.get_user()}


bottle.run(app=app, port=8080)