from flask import Blueprint, render_template, session, request, redirect, url_for
from flask.helpers import flash

from ..function import main_security

admin_routes = Blueprint('admin_routes', __name__,
                        template_folder='templates',
                        static_folder='static')

@admin_routes.route('/')
@admin_routes.route('/dashboard')
def dashboard():
    if main_security.test_session_connected(session):
        return render_template('admin/dashboard.html')
    else:
        return redirect(url_for('main_routes.index'))