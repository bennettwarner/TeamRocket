from tinydb import TinyDB, Query

user_db = TinyDB('users.json')
event_db = TinyDB('events.json')

#user_db.insert({'username': 'john', 'password': '123'})

users = Query()
print(user_db.search(users.username == 'john'))
