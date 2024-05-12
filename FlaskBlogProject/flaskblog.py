from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '3def7a51e14a116fcf6765b908b6222c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    image_file = Column(String(20), nullable=False, default='default.jpg')
    password = Column(String(60), nullable=False)
    post = relationship('Post', backref='author', lazy=True)#Upper case 'P' as we are refrencing the the post class itself
   
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    

class Post(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    content = Column(Text, nullable=False)
    # lower case 'u' as we are referencing the actual user table in the d
    user_id = db.Column(Integer, ForeignKey('user.id'))
    
    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}', '{self.content}')"
    
        
posts = [
    {'author': 'Laila Ebrahim', 'title': 'First Post',
     'content': 'This is the first post.', 'date_posted': 'Aug 10 2002'},
    {'author': 'Lili Ebrahim', 'title': 'Second Post',
     'content': 'This is the second post.', 'date_posted': 'Aug 10 2024'},
    {'author': 'Lolo Ebrahim', 'title': 'Second Post',
     'content': 'This is the Third post.', 'date_posted': 'Aug 11 2024'}
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='login', form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


if __name__ == "__main__":
    app.run()
