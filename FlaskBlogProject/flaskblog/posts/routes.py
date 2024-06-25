from flaskblog import db
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskblog.posts.forms import PostForm
from flaskblog.models import Post
from flask_login import current_user, login_required
from datetime import datetime


posts = Blueprint('posts', __name__)


@posts.route('/new/post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        #the date_posted will be by default equal to current time and date_scheduled will be None
        post = Post(title=form.title.data,
                    content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('update_create_post.html', title='New Post', form=form, legend='New Post')


@posts.route('/new/scheduled/post', methods=['GET', 'POST'])
@login_required
def new_scheduled_post():
    datetime1 = request.form.get('datetime')
    datetime1 = datetime.fromisoformat(datetime1)
    title = request.form['title']
    content = request.form['content']
    now = datetime.utcnow()
    if datetime1 < now:
        return 'False'
    else:
        #only case when the date_posted may be a time in the future is when a post is scheduled and not to be posted yet 
        post = Post(title=title,
                    content=content, user_id=current_user.id,
                    date_scheduled=datetime1, date_posted=datetime1)
        db.session.add(post)
        db.session.commit()
        return 'True'


@posts.route("/post/int:<post_id>")
def post(post_id):
    post = Post.query.filter(Post.date_scheduled == None).get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/int:<post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.filter(Post.date_scheduled == None).get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.date_posted = datetime.utcnow()
        db.session.commit()
        flash('Your Post have been updated successfully!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('update_create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/int:<post_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.filter(Post.date_scheduled == None).get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('main.home'))
