from flask import render_template, request, Blueprint
from flaskblog.main.forms import SearchForm
from flaskblog.models import Post


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.date_scheduled == None).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    # case when user enters a search keyword that is valid
    if form.validate_on_submit():
        keyword = form.Search.data
        #page number will be by default 1
        page = request.args.get('page', 1, type=int)
        #query the database to find posts that it's content has the searched keywords and return a paginate object with only 5 posts arranged desc by date posted
        posts = Post.query.filter(Post.date_scheduled == None).filter(Post.content.ilike('%' + keyword + '%')).order_by(
            Post.date_posted.desc()).paginate(page=page, per_page=5)
        """ send the searched keyword as a variable to the template to be able to pass it
        to the view function again as a query string so in case of requesting the other pages
        the form is not submitted agian so form.Search.data is None so use the value of the keyword query string
        to query the database to get the requested page"""
        return render_template('search.html', title='Search', form=form, posts=posts, keyword=keyword)
    #case when navigating the pages of result of search
    elif request.args.get('page', 1, type=int) and request.args.get('keyword', type=str):
        page = request.args.get('page', 1, type=int)
        keyword = request.args.get('keyword', type=str)
        posts = Post.query.filter(Post.content.ilike('%' + keyword + '%')).order_by(
            Post.date_posted.desc()).paginate(page=page, per_page=5)
        return render_template('search.html', title='Search', form=form, posts=posts, keyword=keyword)
    #case when user request the search route
    return render_template('search.html', title='Search', form=form, posts=None)
