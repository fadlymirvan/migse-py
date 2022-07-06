import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
