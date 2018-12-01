from tinydb import TinyDB, Query
import random

user_db = TinyDB('users.json')
event_db = TinyDB('events.json')

user_db.insert({'id': random.randint(1,9999999999999999), 'username': 'john', 'password': '123'})

users = Query()
current_user = user_db.search(users.username == 'ben')
print(current_user[0])
