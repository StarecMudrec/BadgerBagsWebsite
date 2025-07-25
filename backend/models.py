from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger
from datetime import datetime, timedelta
import uuid  # For generating unique tokens

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
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    price = db.Column(db.Integer)

    def present(self): 
        return {"id": self.id, 
                "img": self.img, 
                "category": self.category, 
                "name": self.name, 
                "description": self.description}

class AllowedAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger, unique=True)
    telegram_username = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AdminToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger, nullable=False)
    token = db.Column(db.String(36), unique=True, nullable=False)  # UUID
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    
    @classmethod
    def create(cls, telegram_id, expires_minutes=5):
        token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(minutes=expires_minutes)
        return cls(
            telegram_id=telegram_id,
            token=token,
            expires_at=expires_at
        )