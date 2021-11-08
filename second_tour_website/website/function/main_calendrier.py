from ctypes import create_string_buffer, create_unicode_buffer
import logging
import traceback
import datetime
from flask.helpers import flash
from copy import deepcopy

import flask

from . import main_database
from ..database.main_database import *

def generation_calendrier():
    # Delete all creneaux
    all_creneaux = CRENEAU.query.all()
    for creneau in all_creneaux:
        db.session.delete(creneau)
    db.session.commit()


    all_candidats = CANDIDATS.query.all()
    all_professeurs = PROFESSEUR.query.all()
    all_choix_matieres = CHOIX_MATIERE.query.all()
    all_matieres = MATIERES.query.all()
    all_series = SERIE.query.all()
    all_salles = SALLE.query.all()


    # Create a var that contain all serie general
    series_generale = []
    for serie in all_series:
        if serie.nom == "Générale":
            series_generale.append(serie.id_serie)            

    # Start with techno serie
    # Create a var that contain the candidates order by techno then general
    candidat_ordened = []
    for candidat in all_candidats:
        if candidat.id_serie in series_generale:
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
            if a_choix_matiere.id_candidat == candidat.id_candidat:
                choix_matiere = a_choix_matiere

        # Get both matiere 
        matiere1, matiere2 = None, None
        for matiere in all_matieres:
            if matiere.id_matiere == choix_matiere.matiere1:
                matiere1 = matiere
            if matiere.id_matiere == choix_matiere.matiere2:
                matiere2 = matiere
        
        # Get prof for each matiere
        professeur_m1, professeur_m2 = [], []
        for professeur in all_professeurs:
            if professeur.matiere == matiere1.id_matiere:
                professeur_m1.append(professeur)
            if professeur.matiere == matiere2.id_matiere:
                professeur_m2.append(professeur)

        # salle for each matiere
        salle_m1, salle_m2 = [], []
        salle_m1_n = []
        for a_prof in professeur_m1:
            salle_m1_n.append(a_prof.salle)
        salle_m2_n = []
        for a_prof in professeur_m2:
            salle_m2_n.append(a_prof.salle)

        for salle in all_salles:
            if salle.id_salle in salle_m1_n:
                salle_m1.append(salle)
            if salle.id_salle in salle_m2_n:
                salle_m2.append(salle)

        # assign matiere
        # FOR THE MOMENT 1 CANDIDAT PER SALLE 
        # NO LUNCH PAUSE

        # Verify the disponibility
        # total time for matiere
        temps_passage_m1 = convert_to_decimal_time(convert_minute_to_string(matiere1.temps_passage if not candidat.tiers_temps else matiere1.temps_passage_tiers_temps))
        temps_passage_m2 = convert_to_decimal_time(convert_minute_to_string(matiere2.temps_passage if not candidat.tiers_temps else matiere2.temps_passage_tiers_temps))
        temps_preparation_m1 = convert_to_decimal_time(convert_minute_to_string(matiere1.temps_preparation if not candidat.tiers_temps else matiere1.temps_preparation_tiers_temps))
        temps_preparation_m2 = convert_to_decimal_time(convert_minute_to_string(matiere2.temps_preparation if not candidat.tiers_temps else matiere2.temps_preparation_tiers_temps))
        

        for x in range(0, 2):

            salle_matiere = salle_m1 if x == 0 else salle_m2
            temps_passage_matiere = temps_passage_m1 if x == 0 else temps_passage_m2
            temps_preparation_matiere = temps_preparation_m1 if x == 0 else temps_preparation_m2
            matiere = matiere1 if x == 0 else matiere2

            heure_debut_preparation_voulue = 8.00
            while heure_debut_preparation_voulue < 20.00:
                for a_salle in salle_matiere:
                    # reset the var
                    aucune_collision = True
                    all_creneaux = CRENEAU.query.all()

                    for creneau in all_creneaux:
                            debut_preparation_creneau = convert_to_decimal_time(creneau.debut_preparation)
                            fin_passage_creneau = convert_to_decimal_time(creneau.fin)
                            for a_matiere in all_matieres:
                                if a_matiere.id_matiere == creneau.id_matiere:
                                    matiere_creneau = a_matiere
                            temps_passage_creneau = convert_to_decimal_time(convert_minute_to_string(matiere_creneau.temps_passage))
                            temps_preparation_creneau = convert_to_decimal_time(convert_minute_to_string(matiere_creneau.temps_preparation))

                            fin_passage_matiere = heure_debut_preparation_voulue + temps_preparation_matiere + temps_passage_matiere

                            # PRINT DEBUG HERE
                            if creneau.id_salle == a_salle.id_salle:
                                # logging.warning("DEBUG : ", "Matiere : ", heure_debut_preparation_voulue, temps_preparation_matiere, temps_passage_matiere, fin_passage_matiere)
                                # logging.warning("DEBUG : ", "Creneau : ", debut_preparation_creneau, temps_preparation_creneau, temps_passage_creneau, fin_passage_creneau)
                                pass

                            # Test if the salle is empty
                            if creneau.id_salle == a_salle.id_salle \
                            and not((heure_debut_preparation_voulue + temps_preparation_matiere >= fin_passage_creneau)
                            or (heure_debut_preparation_voulue + temps_preparation_matiere + temps_passage_matiere <= debut_preparation_creneau + temps_preparation_creneau)):
                                aucune_collision = False
                            
                            # Test if the user don't have already creneau and need a pause
                            if creneau.id_candidat == candidat.id_candidat \
                            and not ((fin_passage_matiere <= debut_preparation_creneau - 0.5)
                            or (heure_debut_preparation_voulue >= fin_passage_creneau + 0.5)):
                                aucune_collision = False

                            # Test for lunch
                            if creneau.id_salle == a_salle.id_salle \
                            and ((heure_debut_preparation_voulue >= 13.00 and heure_debut_preparation_voulue < 14.00)
                            or (fin_passage_matiere > 13.00 and fin_passage_matiere <= 14.00)
                            or (heure_debut_preparation_voulue <= 13.00 and fin_passage_matiere >= 14.00)):
                                aucune_collision = False

                            # Test if the prof don't have too many course
                            if aucune_collision:
                                all_creneau_test_break = CRENEAU.query.order_by(CRENEAU.debut_preparation).filter_by(id_salle=a_salle.id_salle).all()
                                break_time = 0
                                creneau_prec = all_creneau_test_break[0] if len(all_creneau_test_break) > 0 else []
                                x = 0
                                for creneau_test in all_creneau_test_break:
                                    if (res := (convert_to_decimal_time(creneau_test.debut_preparation) - (convert_to_decimal_time(creneau_prec.debut_preparation) + 0.5))) >= 0:
                                        break_time += res
                                    creneau_prec = creneau_test
                                    x += 1
                                    if x >= 4:
                                        if break_time == 0 and convert_to_decimal_time(creneau_prec.debut_preparation) + 0.5 == heure_debut_preparation_voulue:
                                            x = 0
                                            aucune_collision = False
                                            
                            # Test only morning or only afternoon
                            first_creneau = CRENEAU.query.filter_by(id_candidat=candidat.id_candidat).first()
                            if first_creneau \
                            and ((convert_to_decimal_time(first_creneau.debut_preparation) <= 13.00 and heure_debut_preparation_voulue >= 14.00)
                            or (convert_to_decimal_time(first_creneau.debut_preparation) >= 14.00 and heure_debut_preparation_voulue <= 13.00)):
                                aucune_collision = False
                            
                            
                

                    if aucune_collision:
                        # Create the creneau
                        # logging.warning(matiere.id_matiere, heure_debut_preparation_voulue, temps_preparation_matiere, temps_passage_matiere)
                        res = main_database.add_creneau(candidat.id_candidat, matiere.id_matiere, a_salle.id_salle, convert_from_decimal_time(heure_debut_preparation_voulue), convert_from_decimal_time(heure_debut_preparation_voulue + temps_preparation_matiere), convert_from_decimal_time(heure_debut_preparation_voulue + temps_preparation_matiere + temps_passage_matiere))
                        if res[1] == 'danger':
                            logging.warning(res[0])
                        heure_debut_preparation_voulue = 20
                        break
                heure_debut_preparation_voulue += 0.5
    
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
    h, m = int(time/60), int(time%60)
    return f"{h}:{m}"


def test_calendar_complete():
    all_choix_matiere = CHOIX_MATIERE.query.all()
    all_choix_matiere_left = deepcopy(all_choix_matiere) # Because all_choix_matiere is immutable
    all_creneaux = CRENEAU.query.all()

    matiere_left = 0
    for _ in all_choix_matiere:
        if _.matiere1:
            matiere_left += 1
        if _.matiere2:
            matiere_left += 1

    i = 0
    for choix_matiere in all_choix_matiere:
        matiere1, matiere2 = False, False
        for creneau in all_creneaux:
            if creneau.id_candidat == choix_matiere.id_candidat:
                if creneau.id_matiere == choix_matiere.matiere1:
                    matiere1 = True
                    matiere_left -= 1
                elif creneau.id_matiere == choix_matiere.matiere2:
                    matiere2 = True
                    matiere_left -= 1
        if matiere1 and matiere2:
            all_choix_matiere_left.pop(i)
            i -= 1
        i += 1
    


    if matiere_left > 0:
        logging.warning("Le calendrier n'est pas complet :", matiere_left, all_choix_matiere_left)
        text_creneau = 'créneau' if matiere_left <= 1 else 'créneaux'
        return [f'Le calendrier n\'est pas complet, il manque {matiere_left} ' + text_creneau, 'danger']
    else:
        logging.warning("Le calendrier est complet !")
        return ['Calendrier généré avec succès', 'success']