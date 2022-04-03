import logging
from datetime import datetime


from ..main_website import db
import requests
import os


def basic_auth(content: dict = {}):
    return {"username": os.getenv('AUTH_USERNAME'), "password": os.getenv('AUTH_PASSWORD'), "content": content}


def ask_api(what: str, content):
    if(os.getenv("NETWORK_VISU") == "true"):
        requests.post("http://"+os.getenv("LOCAL_IP")+":3000/add", json={
            "type": "trigger",
            "name": "website:api",
            "data": {
                "target": "website:api"
            }
        })

    # if type(content) == list:
    #     content = {content[i]: "" for i in range(0, len(content))}
    url = os.getenv("API_URL") + what
    logging.info("Asking API on : " + str(url) +
                 " BODY : " + str(basic_auth(content)))
    if "/insert/" in url:
        func = requests.put
    elif "/delete/" in url or "/deleteall" in url or "/deletefilter/" in url:
        func = requests.delete
    elif "/updatefilter/" in url:
        func = requests.patch
    else:
        func = requests.post
    return func(url, json=basic_auth(content))


def transform_dict_strptime(table: list, columns: list):
    output = []
    for row in table:
        for column in columns:
            row[column] = datetime.strptime(
                row[column], "%a %b %d %H:%M:%S %Y")
        output.append(row)
    return output
