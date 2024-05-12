from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '3def7a51e14a116fcf6765b908b6222c'
# The SQLALCHEMY_DATABASE_URI configuration variable is used to specify the database URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# is a line of code that initializes a SQLAlchemy object and binds it to the Flask application object app.
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#create an instance of the LoginManager associated to the current app
login_manager = LoginManager(app)
#to define routr to redirect the user when a log in is needed 
login_manager.login_view = 'login'
#to define the styling of the flash message on redirecting to the login view
login_manager.login_message_category = 'info'

from flaskblog import routes