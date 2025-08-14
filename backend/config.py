import os
from hashlib import sha256


class Config:
    # Configuration
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@db:5432/badgerbags"  # SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024