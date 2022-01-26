from dotenv import load_dotenv
from website.main_website import app, db, logging


def main():
    test()
    run(debug_mode=True)


def test():
    # from function import main_test_dependance
    pass

def dotenv_config():
    load_dotenv()

def run(debug_mode=False):
    logging.warning("Run the server")
    # Run the database
    db.create_all()
    
    from website.database.test import insert_user
    insert_user.inser_admin()

    # Run the website
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)


if __name__ == "__main__":
    main()
