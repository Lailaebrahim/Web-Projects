from flask import Flask
from flaskblog.config import Configuration
from flaskblog import db, bcrypt, login_manager, mail, scheduler
from flaskblog.scheduler import schedule_posts


def create_app(config_class=Configuration):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    scheduler.init_app(app)

    @scheduler.task('interval', id='schedule_posts', seconds=60)
    def scheduled_task():
        schedule_posts(app)

    scheduler.start()

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
