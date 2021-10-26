import sqlalchemy

from ...function import main_security
from ..main_database import *

def inser_admin():
    email = 'admin@ac-poitiers.fr'
    password = 'L0calAdmin'
    hashed_password = main_security.hash_password(password)
    user = UTILISATEURS(email, hashed_password, True)
    try:
        db.session.add(user)
        db.session.commit()
        print('L\'utilisateur à bien été crée', 'success')
    except sqlalchemy.exc.IntegrityError:
        print('Cet utilisateur existe déjà')