"""Models for Blogly."""
from typing import DefaultDict
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


DEFAULT_IMAGE_URL = 'https://www.icon0.com/vectors/static2/preview2/stock-photo-people-face-cartoon-icon-design-15029.jpg'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.TEXT,
                           nullable=False
                           )

    last_name = db.Column(db.TEXT,
                          nullable=False)

    image_url = db.Column(db.TEXT,
                          nullable=False,
                          default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="users", cascade="all, delete-orphan")

    def __repr__(self):
        user = self
        return f"<User id={user.id} first_name={user.first_name} last_name={user.last_name} image_url={user.image_url}>"

    @property
    def get_full_name(self):
        user = self
        return f"{user.first_name} {user.last_name}"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.TEXT,
                      nullable=False
                      )

    content = db.Column(db.TEXT,
                        nullable=False
                        )

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref="posts")

    def __repr__(self):
        return f"<Post {self.title} {self.content} {self.created_at} {self.userid}>"
