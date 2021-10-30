from ctypes import create_string_buffer
import traceback
import datetime

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
        professeur_m1, professeur_m2 = None, None
        for professeur in all_professeurs:
            if professeur.matiere == matiere1.id_matiere:
                professeur_m1 = professeur
            if professeur.matiere == matiere2.id_matiere:
                professeur_m2 = professeur

        # salle for each matiere
        salle_m1, salle_m2 = None, None
        salle_m1_n = matiere1.loge if matiere1.loge else professeur_m1.salle
        salle_m2_n = matiere2.loge if matiere2.loge else professeur_m2.salle
        for salle in all_salles:
            if salle.id_salle == salle_m1_n:
                salle_m1 = salle
            if salle.id_salle == salle_m2_n:
                salle_m2 = salle

        # assign matiere
        # FOR THE MOMENT 1 CANDIDAT PER SALLE 
        # NO LUNCH PAUSE

        # Verify the disponibility
        # total time for matiere
        total_time_m1 = convert_to_decimal_time(convert_minute_to_string(matiere1.temps_preparation)) + convert_to_decimal_time(convert_minute_to_string(matiere1.temps_passage))
        total_time_m2 = convert_to_decimal_time(convert_minute_to_string(matiere2.temps_preparation)) + convert_to_decimal_time(convert_minute_to_string(matiere2.temps_passage))
        
        for x in range(0, 2):
            print("User : " + candidat.nom)

            salle_m = salle_m1 if x == 0 else salle_m2
            total_time_m = total_time_m1 if x == 0 else total_time_m2
            matiere = matiere1 if x == 0 else matiere2

            all_creneaux = CRENEAU.query.all()
            i = 8.00
            while i < 20.00:
                print("test for creneau :", i)
                # test if the crenau is free
                free = True
                for creneau in all_creneaux:
                        debut_prepa_decimal = convert_to_decimal_time(creneau.debut_preparation)
                        fin_decimal = convert_to_decimal_time(creneau.fin)

                        # Test if the salle is empty
                        if creneau.id_salle == salle_m.id_salle \
                        and ((i < debut_prepa_decimal and i + total_time_m > fin_decimal)
                        or (i < debut_prepa_decimal and i + total_time_m > debut_prepa_decimal)
                        or (i < fin_decimal and i + total_time_m > debut_prepa_decimal)
                        or (i > debut_prepa_decimal and i + total_time_m < fin_decimal)):
                            free = False
                        
                        # Test if the user don't have already creneau
                        if creneau.id_candidat == candidat.id_candidat \
                        and ((i < debut_prepa_decimal-0.5 and i + total_time_m > fin_decimal+0.5)
                        or (i < debut_prepa_decimal-0.5 and i + total_time_m > debut_prepa_decimal-0.5)
                        or (i < fin_decimal+0.5 and i + total_time_m > debut_prepa_decimal-0.5)
                        or (i > debut_prepa_decimal-0.5 and i + total_time_m < fin_decimal+0.5)):
                            free = False
            

                if free:
                    # Create the creneau
                    res = main_database.add_crenaud(candidat.id_candidat, matiere.id_matiere, salle_m.id_salle, convert_from_decimal_time(i), convert_from_decimal_time(i + total_time_m))
                    print(res[0])
                    i = 20
                i += 0.5
            

def convert_from_decimal_time(decimal):
    hours = int(decimal)
    minutes = (decimal*60) % 60
    return "%d:%02d" % (hours, minutes)

def convert_to_decimal_time(time):
    h, m = time.split(':')
    r = int(h) + float(m)/60
    return r

def convert_minute_to_string(time):
    h, m = int(time/60), int(time%60)
    return f"{h}:{m}"