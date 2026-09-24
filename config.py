import os

class Config:
    SECRET_KEY = "CHANGE_THIS_TO_A_RANDOM_SECRET_KEY"

    SQLALCHEMY_DATABASE_URI = "sqlite:///spacexbot.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_FOLDER = "sessions"
