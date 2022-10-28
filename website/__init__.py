from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path,environ
from flask_login import LoginManager
from dotenv import load_dotenv

env_path='/Users/ritikkarayat/Documents/Flask Api/secrets.env'
load_dotenv(dotenv_path=env_path)
#print(environ.get('SQLITE_SECRET_KEY'))
#print(environ.get('DB_NAME'))


db = SQLAlchemy()
DB_NAME=environ.get('DB_NAME')
print(DB_NAME)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = environ.get('SQLITE_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User,Post, Comment, Like



    with app.app_context():
        create_database()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database():
    if not path.exists("instance/" + DB_NAME):
        db.create_all()
        print("Created database!")

