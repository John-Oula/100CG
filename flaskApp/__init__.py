# from flask.ext.uploads import  UploadSet,configure_uploads,IMAGES


from flaskApp.config import Config
# mysql://root:@qwerty1234!@localhost/CHINAGUIDE
import psycopg2
from flask import Flask


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    from flaskApp.users.routes import users
    from flaskApp.posts.routes import posts
    from flaskApp.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app


from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

bcrypt = Bcrypt()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
