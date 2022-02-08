import logging
from datetime import datetime

from ..main_website import db
import requests
import os

def basic_auth(content: dict = {}):
    return {"username": os.getenv('AUTH_USERNAME'), "password": os.getenv('AUTH_PASSWORD'), "content": content}

def ask_api(what: str, content):
    if type(content) == list:
        content = {content[i]: "" for i in range(0, len(content))}
    url = os.getenv("API_URL") + what
    logging.info("Asking API on : ", url, " BODY : ", basic_auth(content))
    return requests.post(url, json=basic_auth(content))

def transform_dict_strptime(table: list, columns: list):
    output = []
    for row in table:
        for column in columns:
                row[column] = datetime.strptime(row[column], "%a %b %d %H:%M:%S %Y")
        output.append(row)
    return output


from .classes.main_classes import *