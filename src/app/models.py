import os
from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import requests


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    desc = db.Column(db.String(140))
    endpoint = db.Column(db.String(140))
    engine = db.Column(db.String(64))
    key = db.Column(db.String(64))
    type = db.Column(db.String(20))

    def __repr__(self):
        return "<Service {}>".format(self.name)


class Jargon(db.Model):
    __tablename__ = "jargons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    desc = db.Column(db.String(140))
    speakers = db.relationship("User", backref="jargon", lazy="dynamic")
    dialects = db.relationship("Dialect", backref="jargon", lazy="dynamic")

    def __repr__(self):
        return "<Jargon {}>".format(self.name)


class Dialect(db.Model):
    __tablename__ = "dialects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    desc = db.Column(db.String(140))
    inspire = db.Column(db.String(20))
    instruct = db.Column(db.String(1024))
    temperature = db.Column(db.Float)
    jargon_id = db.Column(db.Integer, db.ForeignKey("jargons.id"))

    def __repr__(self):
        return "<Dialect {}>".format(self.name)


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    language = db.Column(db.String(5))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    dialect_id = db.Column(db.Integer, db.ForeignKey("dialects.id"))

    def __repr__(self):
        return "<Message {}>".format(self.body)

    def correct(self):
        message = {"body": self.body, "language": self.language}
        mistakes = []
        replacements = []
        correct_ep = "http://127.0.0.1:8000/api/v1/correct"
        response = requests.post(correct_ep, json=message)
        s = response.status_code
        if s == 200:
            r = response.json()
            correct = r["correct"]
            mistakes = r["mistakes"]
            replacements = r["replacements"]
        else:
            correct = "🤔"

        return correct, mistakes, replacements

    def suggest(self, dialect):
        inspire = ""
        message = {"body": self.body, "language": self.language, "dialect": dialect}
        suggest_ep = "http://127.0.0.1:8000/api/v1/suggest"
        # suggest_ep = (
        #     "https://gfsxubzp3b.execute-api.eu-west-3.amazonaws.com/prod/api/v1/suggest"
        # )
        suggest = ""

        def converttostr(input_seq, seperator):
            # Join all the strings in list
            final_str = seperator.join(input_seq)
            return final_str

        response = requests.post(suggest_ep, json=message)
        s = response.status_code
        if s == 200:
            r = response.json()
            suggest = r["suggestions"]
            inspire = r["inspiration"]
        else:
            suggest = "🤔"

        return inspire, converttostr(suggest, os.linesep)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    quota = db.Column(db.Integer)
    jargon_id = db.Column(db.Integer, db.ForeignKey("jargons.id"))
    messages = db.relationship("Message", backref="author", lazy="dynamic")

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
