from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
from datetime import timedelta
from logging import WARNING, ERROR, FileHandler
import logging
import os
import sys

from sqlalchemy import false
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Global website
app = Flask(__name__)

file_handler = FileHandler(
    os.getcwd() + "/logs/logs_info.txt")
file_handler.setLevel(WARNING)
logging.basicConfig(
    level=WARNING,
    format="%(asctime)s %(message)s",
    handlers=[
        file_handler
    ]
)


# Configure the website
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "HEby4gbqFGFtSCeV"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=3)
app.config['UPLOAD_FOLDER'] = os.getcwd(
) + "/second_tour_website/website/upload"


# Configure the database
mysql = MySQL()

DB_HOST = os.getenv('DB_HOST') if os.getenv('DB_HOST') else 'localhost'
DB_USER = os.getenv('DB_USER') if os.getenv('DB_USER') else 'root'
DB_PWD = os.getenv('DB_PWD') if os.getenv('DB_PWD') else ''
DB_NAME = os.getenv('DB_NAME') if os.getenv('DB_NAME') else 'secondtour'

# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_NAME}'


# app.config['MYSQL_DATABASE_HOST'] = DB_HOST
# app.config['MYSQL_DATABASE_USER'] = DB_USER
# app.config['MYSQL_DATABASE_PASSWORD'] = DB_PWD
# app.config['MYSQL_DATABASE_DB'] = DB_NAME

# mysql.init_app(app)


# SQLITE LOCAL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.sqlite3'

db = SQLAlchemy(app)

# Configure the routes blueprint
from .routes.register_routes import register_routes
from .routes.main_routes import main_routes
from .routes.admin_routes import admin_routes
from .routes.professeur_routes import professeur_routes
app.register_blueprint(main_routes, url_prefix='/')
app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(professeur_routes, url_prefix='/professeur')
app.register_blueprint(register_routes, url_prefix='/register')
