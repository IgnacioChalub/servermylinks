from app import db
from flask_login import UserMixin
from datetime import datetime

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    url = db.Column(db.String(500))
    description = db.Column(db.String(350))
    date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, url, description, user_id):
        self.title = title
        self.url = url
        self.description = description
        #self.date = db.DateTime(timezone=True)
        self.user_id = user_id

    def to_json(self):
        return {
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "date": self.date
        }


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)    
    links = db.relationship('Link')

    def __init__(self, email, password, username):
        self.username = username
        self.password = password
        self.email = email
    
    def to_json_without_password(self):
        return {
            "username": self.username,
            "email": self.email
        }