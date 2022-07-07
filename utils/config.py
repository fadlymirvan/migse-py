import os


# Place to Set or Store Config
class Config:
    # Config of Database which using SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    # JWT Secret Key to Generate JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
