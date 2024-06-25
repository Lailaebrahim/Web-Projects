from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_apscheduler import APScheduler

#initializing those objects in the init file of the main project package so they become easliy accesible from anywhere in the project

# initializes a SQLAlchemy object to create a databse engine and bind it to the app.
db = SQLAlchemy()

# create an instance for Bcrypt to use it for encryption of data
bcrypt = Bcrypt()

# create an instance of the LoginManager associated to the current app
login_manager = LoginManager()

# to define route to redirect the user when a log in is needed
login_manager.login_view = 'users.login'

# to define the styling of the flash message on redirecting to the login view
login_manager.login_message_category = 'info'

# create an instance of the mail object which is the interface to the smtp client provided by flask_mail
mail = Mail()

scheduler = APScheduler()
