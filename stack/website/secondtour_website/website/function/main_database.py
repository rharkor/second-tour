from datetime import datetime, timedelta
import traceback
import logging
from urllib import response

from flask.helpers import flash
from itsdangerous import json

from . import main_security
from ..database.main_database import *

from . import main_email


def delete_all_content():
    # for mapper in db.Model.registry.mappers:
    #     if str(mapper) == "mapped class UTILISATEUR->UTILISATEUR":
    #         continue
    #     db.session.query(mapper).delete()
    response = ask_api("data/deleteall", {})
    if response.status_code != 202:
        logging.warning("Erreur lors de la suppression des données")


def insert_admin():
    response = ask_api("data/insert/utilisateur", {"id_utilisateur": "null", "email": "admin@ac-poitiers.fr",
                       "password": "$p5k2$3e8$AfpOzesj$.KoGR.raCRkA3gne.aZrF1bQobRfdSIH", "admin": "true", "id_professeur": "null"})
    if response.status_code != 201:
        logging.warning("Erreur lors de la suppression des données")


def add_account(email, password, user_type_string, output=False):
    hashed_password = main_security.hash_password(password)
    user_type = True if user_type_string == "Administrateur" else False
    # user = UTILISATEUR(email, hashed_password, user_type, id_prof)
    # try:
    #     if not user.unvalid:
    #         db.session.add(user)
    #         db.session.commit()
    #         if output:
    #             logging.warning('L\'utilisateur a bien été crée')
    #             return (user, ['L\'utilisateur a bien été crée', 'success'])
    #         logging.warning('L\'utilisateur a bien été crée')
    #         return ['L\'utilisateur a bien été crée', 'success']
    #     else:
    #         if output:
    #             return (user, user.unvalid)
    #         return user.unvalid
    try:
        tokens_filter = {"email": email, "admin": user_type_string}
        response = ask_api("data/fetchfilter/token", tokens_filter)
        if response.status_code != 200:
            logging.warning(
                "Impossible de récupérer tout les tokens")
            return ['Impossible de récupérer tout les tokens', 'danger']
        id_prof = response.json()[0]["id_professeur"]

        user = {"id_utilisateur": "null", "email": email, "password": hashed_password,
                "admin": "true" if user_type else "false", "id_professeur": id_prof}
        response = ask_api("data/insert/utilisateur", user)
        if response.status_code != 201:
            logging.warning("Erreur lors de l'insertion d'un utilisateur")
            if output:
                return (user, ["Erreur lors de l'insertion d'un utilisateur", "danger"])
            return "Erreur lors de l'insertion d'un utilisateur", "danger"
        user["id_utilisateur"] = response.json()["id"]
        if output:
            logging.warning('L\'utilisateur a bien été crée')
            return (user, ['L\'utilisateur a bien été crée', 'success'])
        logging.warning('L\'utilisateur a bien été crée')
        return ['L\'utilisateur a bien été crée', 'success']
    except Exception:
        if output:
            logging.warning('Erreur : ' + traceback.logging.warning_exc())
            return (user, ['Erreur : ' + traceback.logging.warning_exc(), 'danger'])
        logging.warning('Erreur : ' + traceback.logging.warning_exc())
        return ['Erreur : ' + traceback.logging.warning_exc(), 'danger']


def add_account_token(email, token, user_type_string, id_prof):
    # Token creation
    user_type = True if user_type_string == "Administrateur" else False
    add_token(email, token, user_type, id_prof)
    logging.warning('Le token a bien été crée')
    return ['L\'email à bien été envoyé', 'success']


def delete_account(id):
    try:
        user = {"id_utilisateur": id, "admin": "false"}
        response = ask_api(f"data/deletefilter/utilisateur", user)
        if response.status_code != 202:
            logging.warning("Impossible de supprimer cet utilisateur")
            return ['Impossible de supprimer cet utilisateur', 'danger']
        return False
        # user = UTILISATEUR.query.filter_by(id=id).one()
        # if user.admin == False:
        #     db.session.delete(user)
        #     db.session.commit()
        #     return False
        # else:
        #     logging.warning('Impossible de supprimer cet utilisateur')
        #     return ['Impossible de supprimer cet utilisateur', 'danger']
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_serie(serie_choice, specialite1, specialite2, ret=False):
    try:
        serie = {"id_serie": "null", "nom": serie_choice, "specialite1": specialite1,
                 "specialite2": specialite2 if specialite2 else "null"}
        response = ask_api("data/insert/serie", serie)
        if response.status_code != 201:
            logging.warning("Erreur lors de l'insertion d'une serie")
            if ret:
                return (["Erreur lors de l'insertion d'une serie", "danger"], serie)
            return "Erreur lors de l'insertion d'une serie", "danger"
        serie["id_serie"] = response.json()["id"]
        if not ret:
            return [['La série a bien été crée', 'success']]
        else:
            return [['La série a bien été crée', 'success'], serie]
        # serie = SERIE(serie_choice, specialite1, specialite2)
        # if not serie.unvalid:
        #     db.session.add(serie)
        #     db.session.commit()
        #     logging.warning('La série a bien été créée')
        #     if not ret:
        #         return [['La série a bien été créée', 'success']]
        #     else:
        #         return [['La série a bien été créée', 'success'], serie]
        # else:
        #     return [serie.unvalid]
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return [['Erreur : ' + traceback.format_exc(), 'danger']]


def update_serie(id, nom, specialite1, specialite2):
    try:
        serie = {"filter": {"id_serie": id}, "data": {"id_serie": id,
                                                      "nom": nom, "specialite1": specialite1, "specialite2": specialite2}}
        response = ask_api("data/updatefilter/serie", serie)
        if response.status_code != 202:
            logging.warning("Erreur lors de l'insertion des séries")
            return "Erreur lors de l'insertion des séries", "danger"

    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_serie(id):
    try:
        candidat_filter = {"id_serie": id}
        response = ask_api("data/fetchfilter/candidat", candidat_filter)
        if response.status_code != 200:
            logging.warning(
                "Impossible de récupérer tout les candidats correspondants à cette série")
            return ['Impossible de récupérer tout les candidats correspondants à cette série', 'danger']
        candidats = response.json()

        for candidat in candidats:
            # delete creneau
            creneau = {"id_candidat": candidat['id_candidat']}
            response = ask_api(f"data/deletefilter/creneau", creneau)
            if response.status_code != 202:
                logging.warning(
                    "Impossible de supprimer les creneaux des candidats correspondants à cette serie")
                return ['Impossible de supprimer les creneaux des candidats correspondants à cette serie', 'danger']
            # delete choix_matiere
            choix_matiere = {"id_candidat": candidat['id_candidat']}
            response = ask_api(
                f"data/deletefilter/choix_matiere", choix_matiere)
            if response.status_code != 202:
                logging.warning(
                    "Impossible de supprimer les choix matiere des candidats correspondants à cette serie")
                return ['Impossible de supprimer les choix matiere des candidats correspondants à cette serie', 'danger']

        response = ask_api(f"data/deletefilter/candidat", candidat_filter)
        if response.status_code != 202:
            logging.warning(
                "Impossible de supprimer les candidats correspondants à cette serie")
            return ['Impossible de supprimer les candidats correspondants à cette serie', 'danger']

        liste_matieres_filter = {"id_serie": id}
        response = ask_api(f"data/fetchfilter/matiere", liste_matieres_filter)
        if response.status_code != 200:
            logging.warning(
                "Impossible de récupérer la liste des matières")
            return ['Impossible de récupérer la liste des matières', 'danger']
        liste_matieres = response.json()

        for matiere in liste_matieres:
            response = ask_api(f"data/deletefilter/liste_matiere",
                               {"id_matiere": matiere["id_matiere"]})
            if response.status_code != 202:
                logging.warning(
                    "Impossible de supprimer le lien de la série avec les professeurs")
                return ['Impossible de supprimer le lien de la série avec les professeurs', 'danger']

        matiere_filter = {"id_serie": id}
        response = ask_api(f"data/deletefilter/matiere", matiere_filter)
        if response.status_code != 202:
            logging.warning(
                "Impossible de supprimer les matieres correspondantes")
            return ['Impossible de supprimer les matieres correspondantes', 'danger']

        serie_filter = {"id_serie": id}
        response = ask_api(f"data/deletefilter/serie", serie_filter)
        if response.status_code != 202:
            logging.warning("Impossible de supprimer cette serie", "danger")
            return ['Impossible de supprimer cette serie', 'danger']

        return False
        # user = SERIE.query.filter_by(id_serie=id).one()
        # # Delete the dependency
        # matieres = MATIERE.query.filter_by(id_serie=id)
        # for matiere in matieres:
        #     db.session.delete(matiere)
        # candidats = CANDIDAT.query.filter_by(id_serie=id)
        # for candidat in candidats:
        #     creneaux = CRENEAU.query.filter_by(id_candidat=candidat.id_candidat)
        #     for crenau in creneaux:
        #         db.session.delete(crenau)
        #     db.session.delete(candidat)
        # db.session.delete(user)
        # db.session.commit()
        # return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_matiere(name, serie_id, temps_preparation, temps_preparation_tiers_temps, temps_passage, temps_passage_tiers_temps, loge, ret=False):
    try:
        serie_filter = {"id_serie": serie_id}
        response = ask_api("data/fetchfilter/serie", serie_filter)
        if response.status_code != 200:
            logging.warning("Erreur lors de la récupération de la serie")
            if ret:
                return ("Erreur lors de la récupération des series", "danger")
            return "Erreur lors de la récupération des series", "danger"
        serie = response.json()[0]
        if serie:
            serie_name = serie["specialite1"] if serie["specialite2"] is None else serie["specialite1"] + \
                "/" + serie["specialite2"]
        else:
            logging.warning(f"Erreur : No serie found at this id ({serie_id})")
            if ret:
                return ("Erreur lors de la récupération de la serie correspondantes", "danger")
            return "Erreur lors de la récupération de la serie correspondantes", "danger"
        name_complete = f"{name} - {serie_name}"

        matiere = {"id_matiere": "null", "id_serie": serie['id_serie'], "nom": name, "nom_complet": name_complete, "temps_preparation": temps_preparation,
                   "temps_preparation_tiers_temps": temps_preparation_tiers_temps, "temps_passage": temps_passage, "temps_passage_tiers_temps": temps_passage_tiers_temps, "loge": loge if loge else "null"}
        response = ask_api("data/insert/matiere", matiere)
        if response.status_code != 201:
            logging.warning("Erreur lors de l'insertion d'une matiere")
            if ret:
                return ("Erreur lors de l'insertion d'une matiere", "danger")
            return "Erreur lors de l'insertion d'une matiere", "danger"
        matiere["id_matiere"] = response.json()["id"]
        if not ret:
            return 'La matiere a bien été créée', 'success'
        else:
            return [['La matiere a bien été créée', 'success'], matiere]

        # serie = int(serie)
        # all_series = SERIE.query.all()
        # serie_name = None
        # for a_serie in all_series:
        #     if a_serie.id_serie == serie:
        #         serie_name = a_serie.specialite1
        #         if a_serie.specialite2 is not None:
        #             serie_name += '/' + a_serie.specialite2
        # if serie_name is None:
        #     logging.warning(f"Erreur : No serie found at this id ({serie})")
        # name_complete = f"{name} - {serie_name}"
        # matiere = MATIERE(serie, name, name_complete, temps_preparation,
        #                    temps_preparation_tiers_temps, temps_passage, temps_passage_tiers_temps, loge)
        # if not matiere.unvalid:
        #     db.session.add(matiere)
        #     db.session.commit()
        #     logging.warning('La matière a bien été créée')
        #     if ret:
        #         return [['La matière a bien été créée', 'success'], matiere]
        #     return ['La matière a bien été créée', 'success']
        # else:
        #     if ret:
        #         return [matiere.unvalid]
        #     return matiere.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        if not ret:
            return [['Erreur : ' + traceback.format_exc(), 'danger']]
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_matiere(id):
    try:
        # liste matiere
        liste_matiere_filter = {"id_matiere": id}
        response = ask_api(
            f"data/deletefilter/liste_matiere", liste_matiere_filter)
        if response.status_code != 202:
            logging.warning(
                "Impossible de supprimer la matière liés au professeurs")
            return ['Impossible de supprimer la matière liés au professeurs', 'danger']
        # creneaux
        creneau_filter = {"id_matiere": id}
        response = ask_api(f"data/deletefilter/creneau", creneau_filter)
        if response.status_code != 202:
            logging.warning(
                "Impossible de supprimer les creneaux liés à la matiere")
            return ['Impossible de supprimer les creneaux liés à la matiere', 'danger']
        # choix matieres
        choix_matiere_filter = {"matiere1": id}
        response = ask_api(
            f"data/deletefilter/choix_matiere", choix_matiere_filter)
        if response.status_code != 202:
            logging.warning(
                "Impossible de supprimer cette matiere dans le choix des candidats")
            return ['Impossible de supprimer cette matiere dans le choix des candidats', 'danger']
        choix_matiere_filter = {"matiere2": id}
        response = ask_api(
            f"data/deletefilter/choix_matiere", choix_matiere_filter)
        if response.status_code != 202:
            logging.warning(
                "Impossible de supprimer cette matiere dans le choix des candidats")
            return ['Impossible de supprimer cette matiere dans le choix des candidats', 'danger']

        matiere_filter = {"id_matiere": id}
        response = ask_api(f"data/deletefilter/matiere", matiere_filter)
        if response.status_code != 202:
            logging.warning("Impossible de supprimer cette matiere")
            return ['Impossible de supprimer cette matiere', 'danger']

        # matiere = MATIERE.query.filter_by(id_matiere=id).one()
        # # Delete the dependency
        # liste_matieres = LISTE_MATIERE.query.filter_by(id_matiere=id)
        # for liste_matiere in liste_matieres:
        #     db.session.delete(liste_matiere)
        # # Delete the dependency
        # creneaux = CRENEAU.query.filter_by(id_matiere=id)
        # for creneau in creneaux:
        #     db.session.delete(creneau)
        # # Delete the dependency
        # matieres1 = CHOIX_MATIERE.query.filter_by(matiere1=id)
        # for matiere_actual in matieres1:
        #     matiere_actual.matiere1 = None
        # # Delete the dependency
        # matieres2 = CHOIX_MATIERE.query.filter_by(matiere2=id)
        # for matiere_actual in matieres2:
        #     matiere_actual.matiere2 = None
        # db.session.delete(matiere)
        # db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_salle(numero, ret=False):
    try:
        salle = {"id_salle": "null", "numero": numero}
        response = ask_api("data/insert/salle", salle)
        if response.status_code != 201:
            # print(numero)
            logging.warning(
                "Erreur lors de l'insertion d'une salle", response.content)
            if ret:
                return (["Erreur lors de l'insertion d'une salle", "danger"], salle)
            return "Erreur lors de l'insertion d'une salle", "danger"
        salle["id_salle"] = response.json()["id"]
        if not ret:
            return ['La salle a bien été crée', 'success']
        else:
            return [['La salle a bien été crée', 'success'], salle]
        # salle = SALLE(numero)
        # if not salle.unvalid:
        #     db.session.add(salle)
        #     db.session.commit()
        #     logging.warning('La salle a bien été crée')
        #     if ret:
        #         return [['La salle a bien été crée', 'success'], salle]
        #     return ['La salle a bien été crée', 'success']
        # else:
        #     if ret:
        #         return [salle.unvalid]
        #     return salle.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def update_salle(id, numero):
    try:
        salle = {"filter": {"id_salle": id}, "data": {
            "id_salle": id, "numero": numero}}
        response = ask_api("data/updatefilter/salle", salle)
        if response.status_code != 202:
            logging.warning("Erreur lors de l'insertion des salles")
            return "Erreur lors de l'insertion des salles", "danger"

    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_salle(id):
    try:
        # update professeur
        professeur = {"filter": {"salle": id}, "data": {"salle": "null"}}
        response = ask_api(f"data/updatefilter/professeur", professeur)
        if response.status_code != 202:
            logging.warning(
                "Impossible de supprimer les professeurs associés à cette salle")
            return ['Impossible de supprimer les professeurs associés à cette salle', 'danger']

        # creneaux
        creneau_filter = {"id_salle": id}
        response = ask_api(f"data/deletefilter/creneau", creneau_filter)
        if response.status_code != 202:
            logging.warning(
                "Impossible de supprimer les creneaux liés à la salle")
            return ['Impossible de supprimer les creneaux liés à la salle', 'danger']
        # matiere
        matiere_filter = {"loge": id}
        response = ask_api(f"data/deletefilter/matiere", matiere_filter)
        if response.status_code != 202:
            logging.warning(
                "Impossible de supprimer les matieres liés à la salle")
            return ['Impossible de supprimer les matieres liés à la salle', 'danger']

        salle_filter = {"id_salle": id}
        response = ask_api(f"data/deletefilter/salle", salle_filter)
        if response.status_code != 202:
            logging.warning("Impossible de supprimer cette salle")
            return ['Impossible de supprimer cette salle', 'danger']

        # salle = SALLE.query.filter_by(id_salle=id).one()
        # # Delete the dependency
        # rows_changed = PROFESSEUR.query.filter_by(
        #     salle=id).update(dict(salle=None))
        # db.session.commit()
        # # Delete the dependency
        # creneaux = CRENEAU.query.filter_by(id_salle=id)
        # for creneau in creneaux:
        #     db.session.delete(creneau)
        # # Delete the dependency
        # matieres = MATIERE.query.filter_by(loge=id)
        # for matiere in matieres:
        #     db.session.delete(matiere)
        # db.session.delete(salle)
        # db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_token(email, token, admin, id_prof):
    token_data = {"id_token": "null", "email": email, "token": str(
        token), "id_professeur": id_prof, "admin": "true" if admin else "false"}
    response = ask_api("data/insert/token", token_data)
    if response.status_code != 201:
        logging.warning("Erreur lors de la creation du token")
    # token_db = TOKEN(email, str(token), id_prof, admin)
    # db.session.add(token_db)
    # db.session.commit()
    main_email.send_email(email, token)


def delete_token(token):
    token_filter = {"token": token}
    response = ask_api("data/deletefilter/token", token_filter)
    if response.status_code != 202:
        logging.warning("Erreur lors de la suppression du token")
    # token_db = TOKEN.query.filter_by(token=token).one()
    # db.session.delete(token_db)
    # db.session.commit()


def add_professeur(email, nom, prenom, salle, matieres=None, token=None, admin=False, heure_arrivee1="08:00", heure_depart1="20:00", heure_arrivee2="08:00", heure_depart2="20:00", heure_arrivee3="08:00", heure_depart3="20:00", ret=False):
    try:
        # user = add_account(email, 'test123', 'Professeur',
        #                    output=True, id_prof=1)

        # if user[1][1] == 'danger':
        #     return user[1]
        # user = user[0]

        professeur = {"id_professeur": "null", "nom": nom,
                      "prenom": prenom, "salle": salle if salle else "null"}
        response = ask_api("data/insert/professeur", professeur)
        if response.status_code != 201:
            logging.warning("Erreur lors de l'insertion d'un professeur")
            if ret:
                return (["Erreur lors de l'insertion d'un professeur", "danger"], professeur)
            return "Erreur lors de l'insertion d'un professeur", "danger"
        professeur["id_professeur"] = response.json()["id"]

        if token:
            add_token(email, token, admin, professeur["id_professeur"])
            logging.warning('Le token a bien été créé')

        if matieres:
            for matiere in matieres:
                liste_matiere = {"id_liste_matiere": "null",
                                 "id_professeur": professeur["id_professeur"], "id_matiere": matiere}
                response = ask_api("data/insert/liste_matiere", liste_matiere)
                if response.status_code != 201:
                    logging.warning(
                        "Erreur lors de l'ajout de la liste matiere")
                    if ret:
                        return (["Erreur lors de l'ajout de la liste matiere", "danger"], liste_matiere)
                    return "Erreur lors de l'ajout de la liste matiere", "danger"

        if type(heure_arrivee1) == str:
            heure_arrivee1 = json.loads(json.dumps(datetime.strptime(
                heure_arrivee1, '%H:%M'), default=myconverter))
            heure_depart1 = json.loads(json.dumps(datetime.strptime(
                heure_depart1, '%H:%M'), default=myconverter))
            heure_arrivee2 = json.loads(json.dumps(datetime.strptime(
                heure_arrivee2, '%H:%M')+timedelta(days=1), default=myconverter))
            heure_depart2 = json.loads(json.dumps(datetime.strptime(
                heure_depart2, '%H:%M')+timedelta(days=1), default=myconverter))
            heure_arrivee3 = json.loads(json.dumps(datetime.strptime(
                heure_arrivee3, '%H:%M')+timedelta(days=2), default=myconverter))
            heure_depart3 = json.loads(json.dumps(datetime.strptime(
                heure_depart3, '%H:%M')+timedelta(days=2), default=myconverter))
        # horaires = HORAIRE(heure_arrivee1, heure_depart1, heure_arrivee2, heure_depart2, heure_arrivee3, heure_depart3, professeur.id_professeur)
        horaire = {"id_horaire": "null", "horaire_arr1": heure_arrivee1, "horaire_dep1": heure_depart1, "horaire_arr2": heure_arrivee2,
                   "horaire_dep2": heure_depart2, "horaire_arr3": heure_arrivee3, "horaire_dep3": heure_depart3, "id_professeur": professeur["id_professeur"]}
        response = ask_api("data/insert/horaire", horaire)
        if response.status_code != 201:
            logging.warning(
                "Erreur lors de l'ajout des horaires du professeur")
            if ret:
                return (["Erreur lors de l'ajout des horaires du professeur", 'danger'], horaire)
            return "Erreur lors de l'ajout des horaires du professeur", "danger"

        if ret:
            return [['Le professeur a bien été créé', 'success'], professeur]
        return ['Le professeur a bien été créé', 'success']

        # professeur = PROFESSEUR(nom, prenom, salle)
        # if not professeur.unvalid:
        #     db.session.add(professeur)
        #     db.session.commit()
        #     logging.warning('Le professeur a bien été créé')

        #     # Token creation
        #     if token:
        #         add_token(email, token, admin, professeur.id_professeur)
        #         logging.warning('Le token a bien été créé')

        #     if matieres:
        #         for matiere in matieres:
        #             liste_matiere = LISTE_MATIERE(
        #                 professeur.id_professeur, matiere)
        #             if not liste_matiere.unvalid:
        #                 db.session.add(liste_matiere)
        #                 db.session.commit()
        #                 logging.warning('La liste matière a bien été ajoutée')

        #     if type(heure_arrivee1) == str:
        #         heure_arrivee1 = datetime.strptime(heure_arrivee1, '%H:%M')
        #         heure_depart1 = datetime.strptime(heure_depart1, '%H:%M')
        #         heure_arrivee2 = datetime.strptime(heure_arrivee2, '%H:%M')+ timedelta(days=1)
        #         heure_depart2 = datetime.strptime(heure_depart2, '%H:%M')+ timedelta(days=1)
        #         heure_arrivee3 = datetime.strptime(heure_arrivee3, '%H:%M')+ timedelta(days=2)
        #         heure_depart3 = datetime.strptime(heure_depart3, '%H:%M')+ timedelta(days=2)
        #     horaires = HORAIRE(heure_arrivee1, heure_depart1, heure_arrivee2, heure_depart2, heure_arrivee3, heure_depart3, professeur.id_professeur)
        #     if not horaires.unvalid:
        #         db.session.add(horaires)
        #         db.session.commit()
        #         logging.warning('L\'horaire a bien été créé')
        #     if ret:
        #         return [['Le professeur a bien été créé', 'success'], professeur]
        #     return ['Le professeur a bien été créé', 'success']
        # else:
        #     if ret:
        #         return [professeur.unvalid]
        #     return professeur.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_professeur_wep(user, nom, prenom, salle, matieres=None):
    try:
        professeur = {"id_professeur": "null",
                      "nom": nom, "prenom": prenom, "salle": salle}
        response = ask_api("data/insert/professeur", professeur)
        if response.status_code != 201:
            logging.warning("Erreur lors de l'insertion d'un professeur")
            return "Erreur lors de l'insertion d'un professeur", "danger"
        professeur["id_professeur"] = response.json()["id"]

        user = {"filter": {"id_utilisateur": user}, "data": {
            "id_professeur": professeur["id_professeur"]}}
        response = ask_api("data/updatefilter/utilisateur", user)
        if response.status_code != 202:
            logging.warning("Erreur lors de la modification de l'utilisateur")
            return "Erreur lors de la modification de l'utilisateur", "danger"

        if matieres:
            for matiere in matieres:
                liste_matiere_insertion = {
                    "id_liste_matiere": "null", "id_professeur": professeur["id_professeur"], "id_matiere": matiere}
                response = ask_api("data/insert/liste_matiere",
                                   liste_matiere_insertion)
                if response.status_code != 201:
                    logging.warning(
                        "Erreur lors de l'insertion des matieres du professeur")
                    return "Erreur lors de l'insertion des matieres du professeur", "danger"

        return ['Le professeur a bien été crée', 'success']

        # professeur = PROFESSEUR(nom, prenom, salle)
        # user_c = UTILISATEUR.query.filter_by(id=user).first()
        # user_c.id_professeur = professeur.id_professeur
        # if not professeur.unvalid:
        #     db.session.add(professeur)
        #     db.session.commit()
        #     logging.warning('Le professeur a bien été crée')

        #     if matieres:
        #         for matiere in matieres:
        #             liste_matiere = LISTE_MATIERE(
        #                 professeur.id_professeur, matiere)
        #             if not liste_matiere.unvalid:
        #                 db.session.add(liste_matiere)
        #                 db.session.commit()
        #                 logging.warning('La liste matière à bien été ajoutée')

        #     return ['Le professeur a bien été crée', 'success']
        # else:
        #     return professeur.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def update_matiere(id, nom, id_serie, temps_preparation, temps_preparation_tiers_temps, temps_passage, temps_passage_tiers_temps, loge):
    try:
        matiere = {"filter": {"id_matiere": id}, "data": {"id_matiere": id, "id_serie": id_serie, "nom": nom, "temps_preparation": temps_preparation,
                                                          "temps_preparation_tiers_temps": temps_preparation_tiers_temps, "temps_passage": temps_passage, "temps_passage_tiers_temps": temps_passage_tiers_temps, "loge": loge}}
        response = ask_api("data/updatefilter/matiere", matiere)
        if response.status_code != 202:
            logging.warning("Erreur lors de l'insertion des matieres")
            return "Erreur lors de l'insertion des matieres", "danger"

    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def update_professeur_wep(id, user, nom, prenom, salle, matieres=None, heure_arrivee1=None, heure_depart1=None, heure_arrivee2=None, heure_depart2=None, heure_arrivee3=None, heure_depart3=None):
    try:
        professeur = {"filter": {"id_professeur": id}, "data": {
            "nom": nom, "prenom": prenom, "salle": salle if salle else "null"}}
        response = ask_api("data/updatefilter/professeur", professeur)
        if response.status_code != 202:
            logging.warning(
                "Erreur lors de l'insertion des matieres du professeur")
            return "Erreur lors de l'insertion des matieres du professeur", "danger"

        if response := delete_liste_matiere_by_prof_id(id):
            return response, "danger"

        if matieres:
            for matiere in matieres:
                liste_matiere_insertion = {
                    "id_liste_matiere": "null", "id_professeur": id, "id_matiere": matiere}
                response = ask_api("data/insert/liste_matiere",
                                   liste_matiere_insertion)
                if response.status_code != 201:
                    logging.warning(
                        "Erreur lors de l'insertion des matieres du professeur")
                    return "Erreur lors de l'insertion des matieres du professeur", "danger"

        heure_arrivee1 = json.loads(json.dumps(datetime.strptime(
            heure_arrivee1, '%H:%M'), default=myconverter))
        heure_depart1 = json.loads(json.dumps(datetime.strptime(
            heure_depart1, '%H:%M'), default=myconverter))
        heure_arrivee2 = json.loads(json.dumps(datetime.strptime(
            heure_arrivee2, '%H:%M')+timedelta(days=1), default=myconverter))
        heure_depart2 = json.loads(json.dumps(datetime.strptime(
            heure_depart2, '%H:%M')+timedelta(days=1), default=myconverter))
        heure_arrivee3 = json.loads(json.dumps(datetime.strptime(
            heure_arrivee3, '%H:%M')+timedelta(days=2), default=myconverter))
        heure_depart3 = json.loads(json.dumps(datetime.strptime(
            heure_depart3, '%H:%M')+timedelta(days=2), default=myconverter))

        horaire = {"filter": {"id_professeur": id}, "data": {"horaire_arr1": heure_arrivee1, "horaire_dep1": heure_depart1,
                                                             "horaire_arr2": heure_arrivee2, "horaire_dep2": heure_depart2, "horaire_arr3": heure_arrivee3, "horaire_dep3": heure_depart3}}
        response = ask_api("data/updatefilter/horaire", horaire)
        if response.status_code != 202:
            logging.warning(
                "Erreur lors de l'insertion des matieres du professeur")
            return "Erreur lors de l'insertion des matieres du professeur", "danger"

        # professeur = PROFESSEUR.query.filter_by(id_professeur=id).first()
        # if professeur:
        #     professeur.id_utilisateur = user
        #     professeur.nom = nom
        #     professeur.prenom = prenom
        #     professeur.salle = salle if salle else None

        #     logging.warning('Le professeur a bien été trouvé')

        #     delete_liste_matiere_by_prof_id(id)

        #     if matieres:
        #         for matiere in matieres:
        #             liste_matiere = LISTE_MATIERE(
        #                 professeur.id_professeur, matiere)
        #             if not liste_matiere.unvalid:
        #                 db.session.add(liste_matiere)
        #                 logging.warning('La liste matière à bien été ajoutée')

        #     horaire = HORAIRE.query.filter_by(id_professeur=id).first()
        #     if horaire:
        #         horaire.horaire_arr1=datetime.strptime(heure_arrivee1, '%H:%M')
        #         horaire.horaire_dep1=datetime.strptime(heure_depart1, '%H:%M')
        #         horaire.horaire_arr2=datetime.strptime(heure_arrivee2, '%H:%M')+ timedelta(days=1)
        #         horaire.horaire_dep2=datetime.strptime(heure_depart2, '%H:%M')+ timedelta(days=1)
        #         horaire.horaire_arr3=datetime.strptime(heure_arrivee3, '%H:%M')+ timedelta(days=2)
        #         horaire.horaire_dep3=datetime.strptime(heure_depart3, '%H:%M')+ timedelta(days=2)

        #     db.session.commit()

        #     return ['Le professeur a bien été modifié', 'success']
        # else:
        #     return professeur.unvalid
        return ['Le professeur a bien été modifié', 'success']
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_liste_matiere_by_prof_id(id_professeur):
    liste_matiere = {"id_professeur": id_professeur}
    response = ask_api("data/deletefilter/liste_matiere", liste_matiere)
    if response.status_code != 202:
        logging.warning(
            "Erreur lors de la suppression du choix des matieres lié au professeur")
        return "Erreur lors de la suppression du choix des matieres lié au professeur", "danger"
    # all_liste_matiere = LISTE_MATIERE.query.filter_by(
    #     id_professeur=id_professeur).all()
    # for liste_matiere in all_liste_matiere:
    #     db.session.delete(liste_matiere)


def delete_professeur(id):
    try:
        # liste matiere
        if res := delete_liste_matiere_by_prof_id(id):
            return res

        # accounts
        accounts = {"id_professeur": id}
        response = ask_api("data/deletefilter/utilisateur", accounts)
        if response.status_code != 202:
            logging.warning(
                "Erreur lors de la suppression du compte du professeur")
            return "Erreur lors de la suppression du compte du professeur", "danger"

        # creneaux
        professeur_filter = {"id_professeur": id}
        response = ask_api("data/fetchfilter/professeur", professeur_filter)
        if response.status_code != 200:
            logging.warning("Erreur lors de la récupération du professeur")
            return "Erreur lors de la récupération du professeur", "danger"
        professeur = response.json()[0]

        creneaux = {"id_salle": professeur['salle']}
        response = ask_api("data/deletefilter/creneau", creneaux)
        if response.status_code != 202:
            logging.warning(
                "Erreur lors de la suppression des creneaux associé à ce professeur")
            return "Erreur lors de la suppression des creneaux associé à ce professeur", "danger"

        # horaires
        horaires = {"id_professeur": id}
        response = ask_api("data/deletefilter/horaire", horaires)
        if response.status_code != 202:
            logging.warning(
                "Erreur lors de la suppression des horaires du professeur")
            return "Erreur lors de la suppression des horaires du professeur", "danger"

        # tokens
        tokens = {"id_professeur": id}
        response = ask_api("data/deletefilter/token", tokens)
        if response.status_code != 202:
            logging.warning(
                "Erreur lors de la suppression des tokens du professeur")
            return "Erreur lors de la suppression des tokens du professeur", "danger"

        professeur = {"id_professeur": id}
        response = ask_api("data/deletefilter/professeur", professeur)
        if response.status_code != 202:
            logging.warning("Erreur lors de la suppression du professeur")
            return "Erreur lors de la suppression du professeur", "danger"

        # professeur = PROFESSEUR.query.filter_by(id_professeur=id).one()

        # liste_matieres = LISTE_MATIERE.query.filter_by(id_professeur=id)
        # for liste_matiere in liste_matieres:
        #     db.session.delete(liste_matiere)

        # accounts = UTILISATEUR.query.filter_by(
        #     id_professeur=professeur.id_professeur)
        # for account in accounts:
        #     db.session.delete(account)

        # creneaux = CRENEAU.query.filter_by(id_salle=professeur.salle)
        # for creneau in creneaux:
        #     db.session.delete(creneau)

        # horaires = HORAIRE.query.filter_by(id_professeur=id)
        # for horaire in horaires:
        #     db.session.delete(horaire)

        # db.session.delete(professeur)
        # db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_candidat(nom, prenom, id_serie, tiers_temps, absent, output=False):
    try:
        candidat = {"id_candidat": "null", "nom": nom, "prenom": prenom, "id_serie": id_serie,
                    "tiers_temps": "true" if tiers_temps == "True" else "false", "absent": "true" if absent == "True" else "false"}
        response = ask_api("data/insert/candidat", candidat)
        if response.status_code != 201:
            logging.warning("Erreur lors de la creation du candidat")
            if output:
                return (candidat, "Erreur lors de la creation du candidat", "danger")
            return "Erreur lors de la creation du candidat", 'danger'
        candidat["id_candidat"] = response.json()["id"]
        if output:
            logging.warning('Le candidat a bien été crée')
            return [candidat, 'Le candidat a bien été crée', 'success']
        return ['Le candidat a bien été crée', 'success']

        # candidat = CANDIDAT(nom, prenom, id_serie,
        #                      True if tiers_temps == "True" else False, True if absent == "True" else False)
        # if not candidat.unvalid:
        #     db.session.add(candidat)
        #     db.session.commit()
        #     if output:
        #         logging.warning('Le candidat a bien été crée')
        #         return [candidat, 'Le candidat a bien été crée', 'success']
        #     return ['Le candidat a bien été crée', 'success']
        # else:
        #     if output:
        #         return (candidat, candidat.unvalid[0], candidat.unvalid[1])
        #     return candidat.unvalid
    except Exception:
        if output:
            logging.warning('Erreur : ' + traceback.format_exc())
            return [candidat, 'Erreur : ' + traceback.format_exc(), 'danger']
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_candidat(id):
    try:
        # choix matiere
        choix_matiere = {"id_candidat": id}
        response = ask_api("data/deletefilter/choix_matiere", choix_matiere)
        if response.status_code != 202:
            logging.warning(
                "Erreur lors de la suppression des choix de matieres du candidat")
            return "Erreur lors de la suppression des choix de matieres du candidat", "danger"

        # creneaux
        creneau = {"id_candidat": id}
        response = ask_api("data/deletefilter/creneau", creneau)
        if response.status_code != 202:
            logging.warning(
                "Erreur lors de la suppression des creneaux du candidat")
            return "Erreur lors de la suppression des creneaux du candidat", "danger"

        candidat_filter = {"id_candidat": id}
        response = ask_api("data/deletefilter/candidat", candidat_filter)
        if response.status_code != 202:
            logging.warning("Erreur lors de la suppression du candidat")
            return "Erreur lors de la suppression du candidat", "danger"

        # candidat = CANDIDAT.query.filter_by(id_candidat=id).one()
        # # Delete the dependency
        # choix_matiere = CHOIX_MATIERE.query.filter_by(id_candidat=id)
        # for choix in choix_matiere:
        #     db.session.delete(choix)
        # # Delete the dependency
        # creneaux = CRENEAU.query.filter_by(id_candidat=id)
        # for creneau in creneaux:
        #     db.session.delete(creneau)
        # db.session.delete(candidat)
        # db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_all_candidats():
    try:
        # choix matiere
        response = ask_api("data/delete/choix_matiere", {})
        if response.status_code != 202:
            logging.warning(
                "Erreur lors de la suppression des choix de matieres du candidat")
            return "Erreur lors de la suppression des choix de matieres du candidat", "danger"

        # creneaux
        response = ask_api("data/delete/creneau", {})
        if response.status_code != 202:
            logging.warning(
                "Erreur lors de la suppression des creneaux du candidat")
            return "Erreur lors de la suppression des creneaux du candidat", "danger"
        response = ask_api("data/delete/candidat", {})

        print(response.text)

        if response.status_code != 202:
            logging.warning("Erreur lors de la suppression des candidats")
            return "Erreur lors de la suppression des candidats", "danger"
        return ['Tous les candidats ont correctement été supprimés !', 'success']
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_choix_matiere(id_candidat, matiere1, matiere2):
    try:
        choix_matiere = {"id_choix_matiere": "null", "id_candidat": id_candidat,
                         "matiere1": matiere1, "matiere2": matiere2}
        response = ask_api("data/insert/choix_matiere", choix_matiere)
        if response.status_code != 201:
            logging.warning("Erreur lors de la creation du choix de matiere")
            return "Erreur lors de la creation du choix de matiere", 'danger'
        return ['Les choix du candidat ont bien été crées', 'success']
        # choix_matiere = CHOIX_MATIERE(id_candidat, matiere1, matiere2)
        # if not choix_matiere.unvalid:
        #     db.session.add(choix_matiere)
        #     db.session.commit()
        #     logging.warning('Les choix du candidat ont bien été crées')
        #     return ['Les choix du candidat ont bien été crées', 'success']
        # else:
        #     return choix_matiere.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_choix_matiere(id):
    try:
        choix_matiere = {"id_choix_matiere": id}
        response = ask_api("data/deletefilter/choix_matiere", choix_matiere)
        if response.status_code != 202:
            logging.warning(
                "Erreur lors de la suppression du choix de matieres")
            return "Erreur lors de la suppression du choix de matieres", "danger"

        # choix_matiere = CHOIX_MATIERE.query.filter_by(
        #     id_choix_matiere=id).one()
        # db.session.delete(choix_matiere)
        # db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_creneau(id_candidat, id_matiere, id_salle, debut_preparation, fin_preparation, fin, auto_commit=True, ret=False):
    try:
        if type(debut_preparation) == str:
            debut_preparation = json.loads(json.dumps(datetime.strptime(
                debut_preparation, '%Y/%m/%d:%H:%M'), default=myconverter))

            fin_preparation = json.loads(json.dumps(datetime.strptime(
                fin_preparation, '%Y/%m/%d:%H:%M'), default=myconverter))

            fin = json.loads(json.dumps(datetime.strptime(
                fin, '%Y/%m/%d:%H:%M'), default=myconverter))
        else:
            debut_preparation = json.loads(json.dumps(
                debut_preparation, default=myconverter))

            fin_preparation = json.loads(json.dumps(
                fin_preparation, default=myconverter))

            fin = json.loads(json.dumps(fin, default=myconverter))
        logging.warning("new Créneau : " + str(id_candidat) +
                        " | " + str(id_matiere) + " | " + str(id_salle))

        creneau = {"id_creneau": "null", "id_candidat": id_candidat, "id_matiere": id_matiere, "id_salle": id_salle,
                   "debut_preparation": debut_preparation, "fin_preparation": fin_preparation, "fin": fin}
        response = ask_api("data/insert/creneau", creneau)
        if response.status_code != 201:
            logging.warning("Erreur lors de la creation du créneau")
            if ret:
                return [creneau, ['Erreur lors de la creation du créneau', 'danger']]
            return "Erreur lors de la creation du créneau", 'danger'

        if ret:
            return [creneau, ['Le créneau a correctement été crée', 'success'], ]
        return ['Le créneau a correctement été crée', 'success']
        # creneau = CRENEAU(id_candidat, id_matiere, id_salle,
        #                   debut_preparation, fin_preparation, fin)
        # if not creneau.unvalid:
        #     db.session.add(creneau)
        #     if auto_commit:
        #         db.session.commit()
        #     logging.warning('Le créneau a correctement été crée')
        #     if ret:
        #         return [['Le créneau a correctement été crée', 'success'], creneau]
        #     return ['Le créneau a correctement été crée', 'success']
        # else:
        #     if ret:
        #         return [creneau.unvalid]
        #     return creneau.unvalid
    except Exception:
        logging.warning(traceback.format_exc())
        logging.warning('Erreur : ' + traceback.format_exc())
        traceback.print_exc()
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_creneau(id):
    try:
        creneau = {"id_creneau": id}
        response = ask_api("data/deletefilter/creneau", creneau)
        if response.status_code != 202:
            logging.warning("Erreur lors de la suppression du creneau")
            return "Erreur lors de la suppression du creneau", "danger"

        # creneau = CRENEAU.query.filter_by(id_creneau=id).one()
        # db.session.delete(creneau)
        # db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_all_creneaux():
    try:
        response = ask_api("data/delete/creneau", {})
        if response.status_code != 202:
            logging.warning("Erreur lors de la supperssion des creneaux")
            return "Erreur lors de la supperssion des creneaux", "danger"
        return ['Tous les créneaux ont correctement été supprimés !', 'success']

        # creneau = CRENEAU.query.all()
        # for creneau in creneau:
        #     logging.warning(f'Suppression des creneaux {creneau.id_creneau}')
        #     result = delete_creneau(creneau.id_creneau)
        #     if result:
        #         flash(result[0], result[1])
        # return ['Tous les créneaux ont correctement été supprimés !', 'success']
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def add_liste_matiere(id_professeur, id_matiere):
    try:
        liste_matiere = {"id_liste_matiere": "null",
                         "id_professeur": id_professeur, "id_matiere": id_matiere}
        response = ask_api("data/insert/liste_matiere", liste_matiere)
        if response.status_code != 201:
            logging.warning("Erreur lors de la creation des listes matieres")
            return "Erreur lors de la creation des listes matieres", 'danger'
        return ['La matière du professeur à bien été ajouté', 'success']

        # liste_matiere = LISTE_MATIERE(id_professeur, id_matiere)
        # if not liste_matiere.unvalid:
        #     db.session.add(liste_matiere)
        #     db.session.commit()
        #     logging.warning('La matière du professeur à bien été ajouté')
        #     return ['La matière du professeur à bien été ajouté', 'success']
        # else:
        #     return liste_matiere.unvalid
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def delete_liste_matiere(id_liste_matiere):
    try:
        liste_matiere = {"id_liste_matiere": id_liste_matiere}
        response = ask_api("data/deletefilter/liste_matiere", liste_matiere)
        if response.status_code != 202:
            logging.warning(
                "Erreur lors de la suppression des listes matieres")
            return "Erreur lors de la suppression des listes matieres", "danger"

        # liste_matiere = LISTE_MATIERE.query.filter_by(
        #     id_liste_matiere=id_liste_matiere).one()
        # db.session.delete(liste_matiere)
        # db.session.commit()
        return False
    except Exception:
        logging.warning('Erreur : ' + traceback.format_exc())
        return ['Erreur : ' + traceback.format_exc(), 'danger']


def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    print(row)
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)
    return rtn_dict


def myconverter(o):
    if isinstance(o, datetime):
        return o.strftime("%a %b %d %H:%M:%S %Y")
