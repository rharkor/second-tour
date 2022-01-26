from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
from datetime import timedelta
from logging import WARNING, ERROR, FileHandler
import logging
import os
import sys
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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:5BU58aH6Qqqv@localhost/dbSecondTour'

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '5BU58aH6Qqqv'
app.config['MYSQL_DATABASE_DB'] = 'dbSecondTour'

mysql.init_app(app)

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
