from flaskblog import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous.serializer import Serializer
from os import urandom
salt = urandom(16)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # Upper case 'P' as we are refrencing the the post class itself
    post = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expiretime=900):
        s = Serializer(app.config['SECRET_KEY'], expiretime)
        data = {'user_id': self.id}
        token = s.dumps(data, salt=salt)
        return token

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt=salt)
            user_id = data['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # lower case 'u' as we are referencing the actual user table in the d
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}', '{self.content}')"
