import os


class configuration():

    # define a secrect key for the app used in serialization, encryption, signing data
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # The SQLALCHEMY_DATABASE_URI configuration variable is used to specify the database URI for SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # adding configuration for the SMTP client to be able to connect to the SMTP server defined in the MAIL_SERVER
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
