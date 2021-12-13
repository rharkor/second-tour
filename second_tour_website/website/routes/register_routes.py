import logging
from flask import Blueprint, render_template, session, request, redirect, url_for, send_file
from flask.helpers import flash

from ..function import main_security, main_sessions, main_database, main_calendrier
from ..database.main_database import *
from ..main_website import app

register_routes = Blueprint('register_routes', __name__,
                            template_folder='templates',
                            static_folder='static')


@register_routes.route('/', methods=['GET', 'POST'])
def register():
    return render_template('register/register.html')
