from flaskblog.models import Post
from flaskblog import db
from datetime import datetime


def schedule_posts(app):
    print("Running schedule_posts job")
    with app.app_context():
        try:
            print('schedule job done')
            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            print(now)
            posts = Post.query.filter(Post.date_scheduled <= now).all()
            print(posts)
            for post in posts:
                post.date_scheduled = None
                db.session.commit()
        except Exception as e:
            print("Error running schedule_posts job: %s", e)
