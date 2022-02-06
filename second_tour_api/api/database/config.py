from .main_database import MySQLDatabase
import os

DB_HOST = os.getenv('DB_HOST') if os.getenv('DB_HOST') else 'localhost'
DB_USER = os.getenv('DB_USER') if os.getenv('DB_USER') else 'root'
DB_PWD = os.getenv('DB_PWD') if os.getenv('DB_PWD') else ''
DB_NAME = os.getenv('DB_NAME') if os.getenv('DB_NAME') else 'secondtour'

db = MySQLDatabase()
db.connect(DB_HOST, DB_USER, DB_PWD, DB_NAME)