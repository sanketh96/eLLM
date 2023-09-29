import datetime

from mongoengine import connect
from flask_mongoengine import MongoEngine

db = MongoEngine()

connect(
    host="mongodb://127.0.0.1:27017/ellm?authSource=admin",
    alias="db",
)


class User(db.Document):
    # id = db.IntField()
    public_id = db.StringField()
    name = db.StringField()
    email = db.StringField()
    password = db.StringField()
    age = db.IntField()
    city = db.StringField()
    state = db.StringField()
    country = db.StringField()
    creation_time = db.DateTimeField(default=datetime.datetime.utcnow)
    meta = {"db_alias": "db"}



class Chat(db.Document):
    # id = db.IntField()
    session_id = db.StringField()
    sender = db.StringField()
    text = db.StringField()
    creation_time = db.DateTimeField(default=datetime.datetime.utcnow)
    meta = {"db_alias": "db"}
