import bottle
from bottle_jwt import (JWTProviderPlugin, jwt_auth_required)
from tinydb import TinyDB, Query


app = bottle.Bottle()

server_secret = 'TEAMROCKET'

class AuthBackend(object):
    users = Query()
    #user = {'id': 1237832, 'username': 'ben', 'password': '123', 'data': {'sex': 'male', 'active': True}}

    def authenticate_user(self, username, password):
        """Authenticate User by username and password.

        Returns:
            A dict representing User Record or None.
        """
        user_db = TinyDB('users.json')
        current_user = user_db.search(self.users.username == username)

        if current_user != [] and username == current_user[0][username] and password == current_user[0][password]:
            return current_user[0]
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