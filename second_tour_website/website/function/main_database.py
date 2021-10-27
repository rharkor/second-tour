import traceback

from . import main_security
from ..database.main_database import *
import sqlalchemy

def add_account(email, password, user_type_string):
    hashed_password = main_security.hash_password(password)
    user_type = True if user_type_string == "Administrateur" else False
    user = UTILISATEURS(email, hashed_password, user_type)
    try:
        if not user.unvalid:
            db.session.add(user)
            db.session.commit()
            return ['L\'utilisateur à bien été crée', 'success']
        else:
            return user.unvalid
    except sqlalchemy.exc.IntegrityError:
        return ['Cet utilisateur existe déjà', 'danger']

def delete_account(id):
    try:
        user = UTILISATEURS.query.filter_by(id=id).one()
        db.session.delete(user)
        db.session.commit()
        return False
    except Exception:
        return ['Erreur : ' + traceback.format_exc(), 'danger']