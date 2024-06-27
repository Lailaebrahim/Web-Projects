from flaskblog import db, bcrypt
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordRequest, ResetPassword
from flaskblog.users.utils import savr_pic, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    # current_user: This is a special variable provided by Flask-Login that always contains the current logged-in user.
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created successfully! Login to access your account.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
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
                return redirect(url_for('main.home'))
        else:
            flash(f"Unsuccessful login! Please check email and password.", 'danger')
    return render_template('login.html', title='login', form=form)


@users.route("/logout")
def logout():
    # logout_user is a method from flask_login used to log out the current user and clear their session.
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
# login_required: This is a decorator that can be used to protect views from being accessed by unauthenticated users.
# When users lied to a view function it will redirect the user to the login page if they are not currently logged in.
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        # if form is valid and the user submitted a profile picture then call saver method
        # which saves the images and create the full path for it
        if form.profile_pic.data:
            pic_name = savr_pic(form.profile_pic.data)
            # then save that path to the current user image file field
            current_user.image_file = pic_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        # commit changes to be saved in th DB
        db.session.commit()
        flash(f'Your account has been updated successfully!', 'success')
        return redirect(url_for('users.account'))
    # if user pressed on my account on the navigation bar which sends a GET request for that url
    elif request.method == 'GET':
        # then value of form fields will be the current values of the logged-in user
        form.username.data = current_user.username
        form.email.data = current_user.email
    # rendering the account.html template with the form values and the current user image file path
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Your Account', image_file=image_file, form=form)


@users.route("/user/string:<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).filter(Post.date_scheduled == None).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['POST', 'GET'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('an email has been sent to you with the instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_password_request'))
    form = ResetPassword()
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)
