from datetime import timedelta
from logging import WARNING, ERROR, FileHandler
import logging
import os
import sys
from fastapi import FastAPI
from typing import Optional
from .database.main_database import MySQLDatabase


sys.path.append(os.path.join(os.path.dirname(__file__)))





description = """
# API

## Functions
This API is here to serve the main website,
you will need to authentificate all your operation on the database. 
"""

tags_metadata = [
    {
        "name": "data",
        "description": "All global cammands, those are generated **automatically**, so in certain case it must be more safe to use dedicated route",
        "externalDocs": {
            "description": "Github documentation of all tables",
            "url": "https://forge.iut-larochelle.fr/lhuort/pts2021_sujet14/-/wikis/Base-de-donn%C3%A9es"
        }
    },
    {
        "name": "candidat",
        "description": "Access to all configured function of the table **candidat**",
    },
    {
        "name": "choix_matiere",
        "description": "Access to all configured function of the table **choix_matiere**",
    },
]





# Global website
app = FastAPI(
    title="SeconTour API",
    description=description,
    version="0.0.1",
    terms_of_service=os.getenv("WEBSITE_URL") + "cgu",
    contact={
        "name": "Dev team",
        "url": "https://www.iut-larochelle.fr/",
        "email": "louis@huort.com",
    },
    license_info={
        "name": "CC BY-NC-ND 4.0",
        "url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
    },
    openapi_tags=tags_metadata
)


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

DB_HOST = os.getenv('DB_HOST') if os.getenv('DB_HOST') else 'localhost'
DB_USER = os.getenv('DB_USER') if os.getenv('DB_USER') else 'root'
DB_PWD = os.getenv('DB_PWD') if os.getenv('DB_PWD') else ''
DB_NAME = os.getenv('DB_NAME') if os.getenv('DB_NAME') else 'secondtour'


if bool(os.getenv('DIST_DB')):
    
    # configure db access
    DB_URI = f"mysql+pymysql://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_NAME}"

    # create the db
    from database import config


    # Import all routes
    from routes.advanced_auto_conf_routes import main_advanced_routes
    app.include_router(
        main_advanced_routes.router,
        prefix="/data",
        tags=["data"]
    )
    
    from routes.basic_tables_routes import candidats_routes
    app.include_router(
        candidats_routes.router,
        prefix="/candidat",
        tags=["candidat"]
    )
    
    from routes.basic_tables_routes import choix_matiere_routes
    app.include_router(
        choix_matiere_routes.router,
        prefix="/choix_matiere",
        tags=["choix_matiere"]
    )
