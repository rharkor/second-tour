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
    except Exception:
        return ['Erreur : ' + traceback.print_exc(), 'danger']

def delete_account(id):
    try:
        user = UTILISATEURS.query.filter_by(id=id).one()
        db.session.delete(user)
        db.session.commit()
        return False
    except Exception:
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def add_serie(serie_choice, specialite1, specialite2):
    try:
        serie = SERIE(serie_choice, specialite1, specialite2)
        if not serie.unvalid:
            db.session.add(serie)
            db.session.commit()
            return ['La série à bien été crée', 'success']
        else:
            return serie.unvalid
    except Exception:
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def delete_serie(id):
    try:
        user = SERIE.query.filter_by(id_serie=id).one()
        db.session.delete(user)
        db.session.commit()
        return False
    except Exception:
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def add_matiere(name, serie, temps_preparation, temps_passage, loge):
    try:
        serie = int(serie)
        all_series = SERIE.query.all()
        serie_name = None
        for a_serie in all_series:
            if a_serie.id_serie == serie:
                serie_name = a_serie.specialite1
                if a_serie.specialite2 is not None:
                    serie_name += '/' + a_serie.specialite2
        if serie_name is None:
            print(f"Erreur : No serie found at this id ({serie})")
        name_complete = f"{name} - {serie_name}"
        matiere = MATIERES(serie, name, name_complete, temps_preparation, temps_passage, loge)
        if not matiere.unvalid:
            db.session.add(matiere)
            db.session.commit()
            return ['La matière à bien été crée', 'success']
        else:
            return matiere.unvalid
    except Exception:
        return ['Erreur : ' + traceback.format_exc(), 'danger']

def delete_matiere(id):
    try:
        matiere = MATIERES.query.filter_by(id_matiere=id).one()
        db.session.delete(matiere)
        db.session.commit()
        return False
    except Exception:
        return ['Erreur : ' + traceback.format_exc(), 'danger']