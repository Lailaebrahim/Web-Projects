from pytz import utc
from flaskblog.models import Post 
from flaskblog import db
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
scheduler = BackgroundScheduler(timezone=utc)


def schedule_posts():
    now = datetime.utcnow()
    # Query the database to get posts that need to be updated
    posts = Post.query.filter(Post.date_scheduled !=
                              None and Post.date_scheduled <= now).all()
    for post in posts:
      post.date_scheduled = 'None'
      db.session.commit()
  

scheduler.add_job(schedule_posts, 'interval',
                  seconds=60)  # Run every 60 seconds
