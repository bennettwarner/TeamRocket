from tinydb import TinyDB, Query

user_db = TinyDB('users.json')
event_db = TinyDB('events.json')

#user_db.insert({'username': 'john', 'password': '123'})

users = Query()
current_user = user_db.search(users.username == 'john')
print(current_user[0]['password'])
