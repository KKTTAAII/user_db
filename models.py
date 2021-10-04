"""Models for Blogly."""
from typing import DefaultDict
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL = "https://scontent.fbkk5-5.fna.fbcdn.net/v/"
"t31.18172-8/20746116_10154702359061231_1407828309154541812_o.jpg?_"
"nc_cat=104&ccb=1-5&_nc_sid=84a396&_nc_ohc=PEj5I9cBUqoAX9ofBUP&_nc_oc"
"=AQlYbIf3oF-fc7fimrwcM_Cl6QI-8JTmHGLxWqk8QwJeFViIR0AJ8-A-uYKW8fM-s8"
"4&_nc_ht=scontent.fbkk5-5.fna&oh=47495007826807b8310ae1611e52db77&oe=618171B7"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.TEXT,
                            nullable=False,
                            )
            
    last_name = db.Column(db.TEXT,
                            nullable=False)

    image_url = db.Column(db.TEXT,
                            nullable=False,
                            default=DEFAULT_IMAGE_URL)
    
    def __repr__(self):
        user = self
        return f"<User id={user.id} first_name={user.first_name} last_name={user.last_name} image_url={user.image_url}>"

    @property                       
    def get_full_name(self):
        user = self
        return f"{user.first_name} {user.last_name}"