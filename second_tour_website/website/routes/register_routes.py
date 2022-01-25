import logging
from flask import Blueprint, render_template, session, request, redirect, url_for, send_file
from flask.helpers import flash
from itsdangerous import exc

from ..function import main_security, main_sessions, main_database, main_calendrier
from ..database.main_database import *
from ..main_website import app

register_routes = Blueprint('register_routes', __name__,
                            template_folder='templates',
                            static_folder='static')


@register_routes.route('/', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        pass
    else:
        token = request.args.get('token')
        try:
            email = TOKEN.query.filter_by(token=token).one().email
            return render_template('register/register.html', token=token, email=email)
        except Exception:
            return render_template('register/register.html', token="error", email="error")
