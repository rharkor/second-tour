from ctypes import create_string_buffer, create_unicode_buffer
import logging
from threading import local
from time import strftime
import traceback
from datetime import date, datetime, timedelta
from flask.helpers import flash
from copy import deepcopy

import flask

from . import main_database
from ..database.main_database import *


def generation_calendrier():
    
    
    # Delete all creneaux
    # all_creneaux = CRENEAU.query.all()
    # for creneau in all_creneaux:
    #     db.session.delete(creneau)
    # db.session.commit()
    response = ask_api("data/delete/creneau", {})
    if response.status_code != 202:
        flash("Une erreur est survenue lors de la suppression des données", "danger")

    response = ask_api("data/fetchmulti", ["candidat", "professeur", "liste_matiere", "choix_matiere", "matiere", "serie", "salle", "creneau", "horaire"])
    if response.status_code != 200:
        flash("Une erreur est survenue lors de la récupération des données", "danger")
    all_candidats, all_professeurs, all_liste_matiere, all_choix_matieres, all_matieres, all_series, all_salles, local_creneau, all_horaires = response.json()
    # all_candidats = CANDIDATS.query.all()
    # all_professeurs = PROFESSEUR.query.all()
    # all_liste_matiere = LISTE_MATIERE.query.all()
    # all_choix_matieres = CHOIX_MATIERE.query.all()
    # all_matieres = MATIERES.query.all()
    # all_series = SERIE.query.all()
    # all_salles = SALLE.query.all()

    # Create a var that contain all serie general
    series_generale = []
    for serie in all_series:
        if serie["nom"] == "Générale":
            series_generale.append(serie["id_serie"])

    # Start with techno serie
    # Create a var that contain the candidates order by techno then general
    candidat_ordened = []
    for candidat in all_candidats:
        if candidat["id_serie"] in series_generale:
            # Push at the end
            candidat_ordened.append(candidat)
        else:
            # Push at the begining
            candidat_ordened.insert(0, candidat)

    # Create the creneau for each candidate
    for candidat in candidat_ordened:
        # Find the choix matiere correspondant
        choix_matiere = None
        for a_choix_matiere in all_choix_matieres:
            if a_choix_matiere["id_candidat"] == candidat["id_candidat"]:
                choix_matiere = a_choix_matiere
        if not choix_matiere:
            continue

        # Get both matiere
        matiere1, matiere2 = None, None
        for matiere in all_matieres:
            if matiere["id_matiere"] == choix_matiere["matiere1"]:
                matiere1 = matiere
            if matiere["id_matiere"] == choix_matiere["matiere2"]:
                matiere2 = matiere

        # Get prof for each matiere
        professeur_m1, professeur_m2 = [], []
        for professeur in all_professeurs:
            for liste_matiere in all_liste_matiere:
                if liste_matiere["id_professeur"] == professeur["id_professeur"]:
                    if matiere1 is not None:
                        if liste_matiere["id_matiere"] == matiere1["id_matiere"]:
                            professeur_m1.append(professeur)
                    if matiere2 is not None:
                        if liste_matiere["id_matiere"] == matiere2["id_matiere"]:
                            professeur_m2.append(professeur)
        

        # salle for each matiere
        salle_m1, salle_m2 = [], []
        salle_m1_n = []
        for a_prof in professeur_m1:
            salle_m1_n.append(a_prof["salle"])
        salle_m2_n = []
        for a_prof in professeur_m2:
            salle_m2_n.append(a_prof["salle"])

        for salle in all_salles:
            if salle["id_salle"] in salle_m1_n:
                salle_m1.append(salle)
            if salle["id_salle"] in salle_m2_n:
                salle_m2.append(salle)

        try:

            # Verify the disponibility
            # total time for matiere
            if (not matiere1):
                temps_passage_m1 = None
            else:
                temps_passage_m1 = timedelta(
                    minutes=matiere1["temps_passage"] if not candidat["tiers_temps"] else matiere1["temps_passage_tiers_temps"])
                temps_preparation_m1 = timedelta(
                    minutes=matiere1["temps_preparation"] if not candidat["tiers_temps"] else matiere1["temps_preparation_tiers_temps"])

            if (not matiere2):
                temps_passage_m2 = None
            else:
                temps_passage_m2 = timedelta(
                    minutes=matiere2["temps_passage"] if not candidat["tiers_temps"] else matiere2["temps_passage_tiers_temps"])
                temps_preparation_m2 = timedelta(
                    minutes=matiere2["temps_preparation"] if not candidat["tiers_temps"] else matiere2["temps_preparation_tiers_temps"])

        except Exception:
            traceback.print_exc()
            logging.warning(traceback.format_exc())

        # Because two choix matieres
        for x in range(0, 2):

            salle_matiere = salle_m1 if x == 0 else salle_m2
            matiere = matiere1 if x == 0 else matiere2
            temps_passage_matiere = temps_passage_m1 if x == 0 else temps_passage_m2
            if (not matiere):
                temps_preparation_matiere = None
            else:
                temps_preparation_matiere = temps_preparation_m1 if x == 0 else temps_preparation_m2

            # For the 3 days of interogation
            for jour_debut_preparation_voulue in range(1, 4):
                heure_debut_preparation_voulue = timedelta(hours=8)
                while heure_debut_preparation_voulue < timedelta(hours=20):

                    for a_salle in salle_matiere:
                        # reset the var
                        aucune_collision = True
                        
                        for creneau in local_creneau:
                            creneau["debut_preparation"] = datetime.strptime(creneau["debut_preparation"], '%a %b %d %H:%M:%S %Y') if type(creneau["debut_preparation"]) == str else creneau["debut_preparation"]
                            creneau["fin_preparation"] = datetime.strptime(creneau["fin_preparation"], '%a %b %d %H:%M:%S %Y') if type(creneau["fin_preparation"]) == str else creneau["fin_preparation"]
                            creneau["fin"] = datetime.strptime(creneau["fin"], '%a %b %d %H:%M:%S %Y') if type(creneau["fin"]) == str else creneau["fin"]
                            
                        
                        
                        all_creneaux = local_creneau
                        


                        for creneau in all_creneaux:
                            if creneau["debut_preparation"].day == jour_debut_preparation_voulue:
                                debut_preparation_creneau = creneau["debut_preparation"]
                                fin_passage_creneau = creneau["fin"]
                                for a_matiere in all_matieres:
                                    if a_matiere["id_matiere"] == creneau["id_matiere"]:
                                        matiere_creneau = a_matiere
                                temps_passage_creneau = datetime.strptime(
                                    convert_minute_to_string(matiere_creneau["temps_passage"]), "%H:%M")
                                temps_preparation_creneau = datetime.strptime(
                                    convert_minute_to_string(matiere_creneau["temps_preparation"]), "%H:%M")
                                if(heure_debut_preparation_voulue is not None and temps_preparation_matiere is not None and temps_passage_matiere is not None):
                                    fin_passage_matiere = heure_debut_preparation_voulue + \
                                        temps_preparation_matiere + temps_passage_matiere

                                # PRINT DEBUG HERE
                                if creneau["id_salle"] == a_salle["id_salle"]:
                                    # logging.warning("DEBUG : ", "Matiere : ", heure_debut_preparation_voulue, temps_preparation_matiere, temps_passage_matiere, fin_passage_matiere)
                                    # logging.warning("DEBUG : ", "Creneau : ", debut_preparation_creneau, temps_preparation_creneau, temps_passage_creneau, fin_passage_creneau)
                                    pass

                                # Test if the salle is empty
                                if(matiere is not None and heure_debut_preparation_voulue is not None and temps_preparation_matiere is not None and temps_passage_matiere is not None):
                                    if creneau["id_salle"] == a_salle["id_salle"] \
                                        and not((heure_debut_preparation_voulue + temps_preparation_matiere >= timedelta(hours=fin_passage_creneau.hour, minutes=fin_passage_creneau.minute))
                                                or (heure_debut_preparation_voulue + temps_preparation_matiere + temps_passage_matiere <= timedelta(hours=(debut_preparation_creneau.hour + temps_preparation_creneau.hour), minutes=(debut_preparation_creneau.minute + temps_preparation_creneau.minute)))):
                                        aucune_collision = False
                                
                                # Test if the user don't have already creneau and need a pause
                                delta_m30 = (
                                    debut_preparation_creneau - timedelta(minutes=30))
                                delta_p30 = (fin_passage_creneau +
                                             timedelta(minutes=30))


                                if creneau["id_candidat"] == candidat["id_candidat"] \
                                    and not ((fin_passage_matiere <= timedelta(hours=delta_m30.hour, minutes=delta_m30.minute))
                                             or (heure_debut_preparation_voulue >= timedelta(hours=delta_p30.hour, minutes=delta_p30.minute))):
                                    aucune_collision = False

                                # Test for lunch
                                if creneau["id_salle"] == a_salle["id_salle"] \
                                    and ((heure_debut_preparation_voulue >= timedelta(hours=13) and heure_debut_preparation_voulue < timedelta(hours=14))
                                         or (fin_passage_matiere > timedelta(hours=13) and fin_passage_matiere <= timedelta(hours=14))
                                         or (heure_debut_preparation_voulue <= timedelta(hours=13) and fin_passage_matiere >= timedelta(hours=14))):
                                    aucune_collision = False

                                # Test if the prof don't have too many course
                                if aucune_collision:

                                    local_creneau_test_break = local_creneau
                                    local_creneau_test_break.sort(key=order_by)
                                    local_creneau_test_break_filtered = filter(lambda creneau: creneau["id_salle"] == a_salle["id_salle"], local_creneau_test_break)
                                                                            
                                    all_creneau_test_break = list(local_creneau_test_break_filtered)
                                    break_time = 0
                                    creneau_prec = all_creneau_test_break[0] if len(
                                        all_creneau_test_break) > 0 else []
                                    x = 0
                                    for creneau_test in all_creneau_test_break:
                                        if (res := (creneau_test["debut_preparation"] - (creneau_prec["debut_preparation"] + timedelta(minutes=30)))) >= timedelta(minutes=0):
                                            break_time += res.seconds / \
                                                3600 + (res.seconds % 3600)
                                        creneau_prec = creneau_test
                                        x += 1
                                        if x >= 4:
                                            if break_time == 0 and creneau_prec["debut_preparation"] + timedelta(minutes=30) == heure_debut_preparation_voulue:
                                                x = 0
                                                aucune_collision = False

                                # Test only morning or only afternoon
                                first_creneau = list(filter(lambda creneau: creneau["id_candidat"] == candidat["id_candidat"], local_creneau))
                                first_creneau = first_creneau[0] if first_creneau else None
                                if first_creneau \
                                    and (((first_creneau["debut_preparation"].hour) <= 13 and heure_debut_preparation_voulue >= timedelta(hours=14))
                                         or ((first_creneau["debut_preparation"].hour) >= 14 and heure_debut_preparation_voulue <= timedelta(hours=13))):
                                    aucune_collision = False

                            # Test both same day
                            first_creneau = list(filter(lambda creneau: creneau["id_candidat"] == candidat["id_candidat"], local_creneau))
                            first_creneau = first_creneau[0] if first_creneau else None
                            if first_creneau \
                                    and (first_creneau["debut_preparation"].day != jour_debut_preparation_voulue):
                                aucune_collision = False

                            # if first_creneau and jour_debut_preparation_voulue == 1:
                            #     print(aucune_collision)
                            #     if(matiere is not None and heure_debut_preparation_voulue is not None and temps_preparation_matiere is not None and temps_passage_matiere is not None):
                            #         print("Validate")
                            #         heure_debut_preparation_voulue_datetime = datetime.strptime(
                            #         f'{jour_debut_preparation_voulue}/{datetime.now().month}/{datetime.now().year} ' + str(heure_debut_preparation_voulue), '%d/%m/%Y %H:%M:%f')
                            #         fin_preparation_matiere_datetime = datetime.strptime(f'{jour_debut_preparation_voulue}/{datetime.now().month}/{datetime.now().year} ' + str((
                            #         heure_debut_preparation_voulue + temps_preparation_matiere)), '%d/%m/%Y %H:%M:%f')
                            #         fin_passage_matiere_datetime = datetime.strptime(f'{jour_debut_preparation_voulue}/{datetime.now().month}/{datetime.now().year} ' + str((
                            #         heure_debut_preparation_voulue + temps_preparation_matiere + temps_passage_matiere)), '%d/%m/%Y %H:%M:%f')
                            #         res = main_database.add_creneau(candidat.id_candidat, matiere.id_matiere, a_salle.id_salle,
                            #                                     heure_debut_preparation_voulue_datetime, fin_preparation_matiere_datetime, fin_passage_matiere_datetime)
                            #         print(res)
                        
                        for professeur in all_professeurs:
                            for liste_matiere in all_liste_matiere:
                                if liste_matiere["id_professeur"]==professeur["id_professeur"] and liste_matiere["id_matiere"]==matiere["id_matiere"]:
                                    for horaire in all_horaires:
                                        if horaire["id_professeur"] == professeur["id_professeur"]:  
                                            heure_debut_preparation_voulue_datetime = datetime.strptime(
                                                f'{jour_debut_preparation_voulue}/{datetime.now().month}/{datetime.now().year} ' + str(heure_debut_preparation_voulue), '%d/%m/%Y %H:%M:%f')
                                            horaire_arr = datetime.strptime(horaire["horaire_arr"+str(int(jour_debut_preparation_voulue))], '%a %b %d %H:%M:%S %Y')
                                            horaire_dep = datetime.strptime(horaire["horaire_dep"+str(int(jour_debut_preparation_voulue))], '%a %b %d %H:%M:%S %Y')
                                            fin_passage_matiere_datetime = datetime.strptime(f'{jour_debut_preparation_voulue}/{datetime.now().month}/{datetime.now().year} ' + str((heure_debut_preparation_voulue + temps_preparation_matiere + temps_passage_matiere)), '%d/%m/%Y %H:%M:%f')
                                            if int(horaire_arr.strftime('%d'))==int(jour_debut_preparation_voulue) and (horaire_arr.strftime('%H:%M:%S')>heure_debut_preparation_voulue_datetime.strftime('%H:%M:%S') or horaire_dep.strftime('%H:%M:%S')<fin_passage_matiere_datetime.strftime('%H:%M:%S')):
                                                aucune_collision = False
                                                

                        if aucune_collision and not candidat["absent"]:
                            # Create the creneau
                            # logging.warning(matiere.id_matiere, heure_debut_preparation_voulue, temps_preparation_matiere, temps_passage_matiere)
                            if(matiere is not None and heure_debut_preparation_voulue is not None and temps_preparation_matiere is not None and temps_passage_matiere is not None):
                                heure_debut_preparation_voulue_datetime = datetime.strptime(
                                    f'{jour_debut_preparation_voulue}/{datetime.now().month}/{datetime.now().year} ' + str(heure_debut_preparation_voulue), '%d/%m/%Y %H:%M:%f')
                                fin_preparation_matiere_datetime = datetime.strptime(f'{jour_debut_preparation_voulue}/{datetime.now().month}/{datetime.now().year} ' + str((
                                    heure_debut_preparation_voulue + temps_preparation_matiere)), '%d/%m/%Y %H:%M:%f')
                                fin_passage_matiere_datetime = datetime.strptime(f'{jour_debut_preparation_voulue}/{datetime.now().month}/{datetime.now().year} ' + str((
                                    heure_debut_preparation_voulue + temps_preparation_matiere + temps_passage_matiere)), '%d/%m/%Y %H:%M:%f')
                                res = main_database.add_creneau(candidat["id_candidat"], matiere["id_matiere"], a_salle["id_salle"],
                                                                heure_debut_preparation_voulue_datetime, fin_preparation_matiere_datetime, fin_passage_matiere_datetime, auto_commit=False, ret=True)
                                if res[1][1] == 'danger':
                                    print(res)
                                    logging.warning(res[1][0])
                                else:
                                    local_creneau.append(res[0])
                            heure_debut_preparation_voulue = timedelta(
                                hours=20)
                            break
                    heure_debut_preparation_voulue += timedelta(minutes=30)

    # commit
    db.session.commit()
    
    result = test_calendar_complete()
    flash(result[0], result[1])


def convert_from_decimal_time(decimal):
    hours = int(decimal)
    minutes = (decimal*60) % 60
    res = "%02d:%02d" % (hours, minutes)
    return res


def convert_to_decimal_time(time):
    h, m = time.split(':')
    r = int(h) + float(m)/60
    r = round(r, 2)
    return r


def convert_minute_to_string(time):
    h, m = int(time/60), int(time % 60)
    return f"{h}:{m}"

def order_by(e):
  return e["debut_preparation"]


def test_calendar_complete():
    response = ask_api("data/fetchmulti", ["creneau", "candidat", "choix_matiere"])
    if response.status_code != 200:
        flash("Une erreur est survenue lors de la récupération des données", "danger")
    all_creneaux, all_candidats, all_choix_matiere = response.json()
    
    # all_choix_matiere = CHOIX_MATIERE.query.all()
    # Because all_choix_matiere is immutable
    all_choix_matiere_left = deepcopy(all_choix_matiere)
    
    
    # all_creneaux = CRENEAU.query.all()
    # all_candidats = CANDIDATS.query.all()

    matiere_left = 0
    for _ in all_choix_matiere:
        if _["matiere1"]:
            matiere_left += 1
        if _["matiere2"]:
            matiere_left += 1

    i = 0
    for choix_matiere in all_choix_matiere:
        candidat = None
        for a_candidat in all_candidats:
            if a_candidat["id_candidat"] == choix_matiere["id_candidat"]:
                candidat = a_candidat
        matiere1, matiere2 = False, False
        for creneau in all_creneaux:
            if creneau["id_candidat"] == choix_matiere["id_candidat"]:
                if creneau["id_matiere"] == choix_matiere["matiere1"]:
                    matiere1 = True
                    matiere_left -= 1
                elif creneau["id_matiere"] == choix_matiere["matiere2"]:
                    matiere2 = True
                    matiere_left -= 1
        if candidat["absent"]:
            if not matiere1:
                matiere_left -= 1 
            else:
                matiere1 = True
            if not matiere2:
                matiere_left -= 1 
            else:
                matiere2 = True
        if matiere1 and matiere2:
            all_choix_matiere_left.pop(i)
            i -= 1
        i += 1

    if matiere_left > 0:
        logging.warning("Le calendrier n'est pas complet")
        text_creneau = 'créneau' if matiere_left <= 1 else 'créneaux'
        return [f'Le calendrier n\'est pas complet, il manque {matiere_left} ' + text_creneau, 'danger']
    else:
        logging.warning("Le calendrier est complet !")
        return ['Calendrier généré avec succès', 'success']
