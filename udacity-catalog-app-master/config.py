import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Auth:
    CLIENT_ID = ('688061596571-3c13n0uho6qe34hjqj2apincmqk86ddj' '.apps.googleusercontent.com')
    CLIENT_SECRET = 'JXf7Ic_jfCam1S7lBJalDyPZ'
    REDIRECT_URI = 'http://127.0.0.1:5000/oauth2callback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'


class Config:
    APP_NAME = "Test Google Login"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret" 


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///catalog.db'


class ProdConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///catalog.db'


config = {
"dev": DevConfig,
"prod": ProdConfig,
"default": DevConfig
}