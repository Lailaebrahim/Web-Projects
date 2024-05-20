from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
import os
load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# The SQLALCHEMY_DATABASE_URI configuration variable is used to specify the database URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# initializes a SQLAlchemy object and binds it to the Flask application object app.
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# create an instance of the LoginManager associated to the current app
login_manager = LoginManager(app)
# to define route to redirect the user when a log in is needed
login_manager.login_view = 'login'
# to define the styling of the flash message on redirecting to the login view
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)
from flaskblog import routes