import os
from hashlib import sha256


class Config:
    # Configuration
    JWT_SECRET_KEY = "COOL"  # Replace with your actual secret key
    BOT_TOKEN_HASH = sha256("7754568533:AAFtq5XtPEQ_Ivl1NudfB2TzFshkjOeSBS4".encode())  # Replace with your actual token
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@db:5432/badgerbags"  # SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")