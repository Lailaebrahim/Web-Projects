import secrets
import os
from PIL import Image
from flaskblog import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    # current_user: This is a special variable provided by Flask-Login that always contains the current logged-in user.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_pwd)
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

# Method to save profile pics as static files and return the path of image


def savr_pic(form_profile_pic):
    # creating a random hex token to name the image so pathes saved in DB don't repeat
    random_hex = secrets.token_hex(8)
    # using os.path methods to get the extension of the uploaded image
    _, fext = os.path.splitext(form_profile_pic.filename)
    # profile picture file name is the generasted randon hex token and the extension
    pic_name = random_hex + fext
    # creating the full path of the profile picture so it can be used to be rendered by templates
    pic_path = os.path.join(app.root_path, 'static/profile_pics', pic_name)
    # Resizing image so it want take up much space
    input_size = (125, 125)
    i = Image.open(form_profile_pic)
    i.thumbnail(input_size)
    i.save(pic_path)
    if current_user.image_file != None:
        # deleting the old image from the static folder
        os.remove(os.path.join(app.root_path,
                  'static/profile_pics', current_user.image_file))
    return pic_name


@app.route("/account", methods=['GET', 'POST'])
# login_required: This is a decorator that can be used to protect views from being accessed by unauthenticated users.
# When applied to a view function it will redirect the user to the login page if they are not currently logged in.
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        # if form is valid and the user submited a profile picture then call saver method which saves the images and create the full path for it
        if form.profile_pic.data:
            pic_name = savr_pic(form.profile_pic.data)
            # then save that path to the current user image file field
            current_user.image_file = pic_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        # commit changes to be saved in th DB
        db.session.commit()
        flash(f'Your account has been updated successfully!', 'success')
        return redirect(url_for('account'))
    # if user pressed on my account on the navigation bar which sends a GET request for that url
    elif request.method == 'GET':
        # then value of form fields will be the current values of the logged in user
        form.username.data = current_user.username
        form.email.data = current_user.email
    # rendering the account.html template with the form values and the current user image file path
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Your Account', image_file=image_file, form=form)


@app.route('/new/post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('update_create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/post/int:<post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/int:<post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('update_create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/int:<post_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully.', 'success')
    return redirect(url_for('home'))


@app.route("/user/string:<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)
