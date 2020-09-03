# init.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from flask import Blueprint
from flask import request, redirect, url_for, render_template, send_from_directory, Flask
import pandas as pd 
from flask_login import login_required, current_user
from csv import reader
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

application = Flask(__name__)

# CONFIGURATION
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
application.config['SECRET_KEY'] = 'C769412D336F9603B1D507F64C13CC4799C8DFF4950A92522C34AA0270A04BE4'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# LIMIT UPLOAD SIZE
application.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

    #
db.init_app(application)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(application)

from .models import User

@login_manager.user_loader
def load_user(user_id):
# since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
application.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
application.register_blueprint(main_blueprint)

    

