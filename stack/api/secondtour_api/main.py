from dotenv import load_dotenv
load_dotenv()
from api.main_api import app, logging

def main(debug_mode=True):
    run(debug_mode=debug_mode)


def run(debug_mode=False):
    logging.warning("Run the server")

    # Run the api
    app.run(host="0.0.0.0", port=443, debug=debug_mode)


if __name__ == "__main__":
    main()
