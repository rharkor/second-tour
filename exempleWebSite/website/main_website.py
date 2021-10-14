from flask import Flask, render_template


class Website:
    def __init__(self):
        self.app = Flask(__name__)

        # Create the route
        self.create_route()

    def run(self):
        self.app.run()

    def create_route(self):
        @self.app.route('/')
        @self.app.route('/index')
        def index():
            return render_template('index.html')

        @self.app.route('/hello/<phrase>')
        def hello(phrase):
            return phrase
