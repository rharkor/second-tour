from flask import Blueprint, render_template, session, request, redirect, url_for
from flask.helpers import flash

from ..function import main_security
from ..database.main_database import *

admin_routes = Blueprint('admin_routes', __name__,
                        template_folder='templates',
                        static_folder='static')

@admin_routes.route('/')
@admin_routes.route('/acceuil')
def acceuil():
    if main_security.test_session_connected(session, True):
        return render_template('admin/acceuil.html')
    else:
        return redirect(url_for('main_routes.connexion'))

@admin_routes.route('/candidats')
def candidats():
    if main_security.test_session_connected(session, True):
        return render_template('admin/candidats.html')
    else:
        return redirect(url_for('main_routes.connexion'))

@admin_routes.route('/salles')
def salles():
    if main_security.test_session_connected(session, True):
        return render_template('admin/salles.html')
    else:
        return redirect(url_for('main_routes.connexion'))
 
@admin_routes.route('/professeurs')
def professeurs():
    if main_security.test_session_connected(session, True):
        return render_template('admin/professeurs.html')
    else:
        return redirect(url_for('main_routes.connexion'))

@admin_routes.route('/series')
def series():
    if main_security.test_session_connected(session, True):
        return render_template('admin/series.html')
    else:
        return redirect(url_for('main_routes.connexion'))
        
@admin_routes.route('/matieres')
def matieres():
    if main_security.test_session_connected(session, True):
        return render_template('admin/matieres.html')
    else:
        return redirect(url_for('main_routes.connexion'))

@admin_routes.route('/comptes')
def comptes():
    if main_security.test_session_connected(session, True):
        all_users = UTILISATEURS.query.all()
        return render_template('admin/comptes.html', all_users=all_users)
    else:
        return redirect(url_for('main_routes.connexion'))

@admin_routes.route('/deconnexion')
def deconnexion():
    if session['email']:
        session.pop('email', None)
    if session['password']:
        session.pop('password', None)
    flash('Vous avez correment été déconnecté', 'primary')
    return redirect(url_for('main_routes.index'))