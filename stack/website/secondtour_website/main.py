import traceback
from dotenv import load_dotenv
load_dotenv()
import logging
import requests
import os
from website.main_website import app, db, logging


def ask_api(what: str):
    url = os.getenv("API_URL") + what

    logging.info("Asking API on : " + url)
    return requests.get(url)


def main(debug_mode=True, dev=False):
    # test(dev)
    run(debug_mode=debug_mode)


def test(dev):
    # from function import main_test_dependance
    try:
        response = ask_api("version")
        if response.status_code != 200:
            raise Exception
    except Exception as e:
        logging.warning("Vérifiez que l'Api est bien lancée.")
        traceback.print_exc()
        quit("L'api n'est pas lancée")


def run(debug_mode=False):
    website_url = 'secondtour.vieljeux.yetixdev.com:8000'
    app.config['SERVER_NAME'] = website_url
    logging.warning("Run the server")
    # Create db with the framwork sql alchemy
    # db.create_all()

    # from website.database.test import insert_user
    # insert_user.inser_admin()

    # Run the website
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)


if __name__ == "__main__":
    main()
