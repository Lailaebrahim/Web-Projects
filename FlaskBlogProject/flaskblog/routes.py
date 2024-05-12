from flaskblog import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


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
    # current_user: This is a special variable provided by Flask-Login that always contains the current logged-in user.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created successfully! Login to access your acount.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # login_user: This function is used to log in a user by associating a user object with the current session.
            # It takes one argument, which is the user object to be logged in.
            login_user(user, remember=form.remember.data)
            next_route = request.args.get('next')
            if next_route != None:
                return redirect(next_route)
            else:
                return redirect(url_for('home'))   
        else:
            flash(f"Unsuccesfull login! Please check email and password.", 'danger')
    return render_template('login.html', title='login', form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/logout")
def logout():
    # logout_user is a method from flask_login used to log out the current user and clear their session.
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
# login_required: This is a decorator that can be used to protect views from being accessed by unauthenticated users.
# When applied to a view function it will redirect the user to the login page if they are not currently logged in.
@login_required
def account():
    return render_template('account.html', title='Your Account')
