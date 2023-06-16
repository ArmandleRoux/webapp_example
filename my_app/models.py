from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(250))
    fav_colour = db.Column(db.String(25))
    birth_date = db.Column(db.Date)
    
    def get_id(self):
        return self.username