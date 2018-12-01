import bottle
from bottle_jwt import (JWTProviderPlugin, jwt_auth_required)
from tinydb import TinyDB, Query

user_db = TinyDB('users.json')
event_db = TinyDB('events.json')

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