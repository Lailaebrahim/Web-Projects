from flask import render_template, request, Blueprint
from flaskblog.main.forms import SearchForm
from flaskblog.models import Post
from sqlalchemy import func

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        keyword = form.Search.data
        posts = Post.query.filter(func.lower(Post.title).like(f'%{keyword}%')).all()
        return render_template('search.html', title='Search', form=form, posts=posts)
    return render_template('search.html', title='Search', form=form, posts=None)
