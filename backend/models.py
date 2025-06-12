from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger

db = SQLAlchemy()

class AllowedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)


class AuthToken(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(BigInteger, nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img = db.Column(db.String)
    category = db.Column(db.String(20))
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    price = db.Column(db.Integer)

    def present(self): 
        return {"id": self.id, 
                "img": self.img, 
                "category": self.category, 
                "name": self.name, 
                "description": self.description}