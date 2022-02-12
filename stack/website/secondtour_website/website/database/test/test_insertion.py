
from dotenv import load_dotenv
from faker import Faker
from tqdm import tqdm
import random

faker = Faker("fr_FR")

load_dotenv()
from website.function import main_database
    


def main_insert():
    '''In this test we will generate _candidates for _teachers'''
    
    # First of all we suppress all the data
    main_database.delete_all_content()
    
    # Insert admin
    main_database.insert_admin()
    
    
    
    # serie
    matieres = []
    
    serie_type = ['Générale', 'Technologique']
    techno_subjects = ['STMG', 'STI2D']
    gene_subjects = ['SI', 'SVT', 'Physique', 'SES', 'Mathématiques']
    
    series = []
    for i in tqdm (range (random.randint(3,len(techno_subjects)+len(gene_subjects))), desc="Uploading 'Series'"):
        output = [['', 'danger']]
        while output[0][1] == 'danger':
            serie = faker.word(serie_type)
            if serie == 'Générale':
                sub1, sub2 = faker.words(2, gene_subjects, True)
            else:
                sub1, sub2 = faker.word(techno_subjects), None
            correct = True
            if series:
                for a_serie in series:
                    if a_serie['nom'] == serie and a_serie['specialite1'] == sub1 and sub2 == None:
                        correct = False
            if correct:
                output = main_database.add_serie(serie, sub1 ,sub2, ret=True)
                            
                try:
                    series.append(output[1])
                    all_names_possible = ['Francais', 'Philosophie']
                    for name in all_names_possible:
                        temps_preparation = 30
                        temps_passage = 30
                        loge = None
                        temps_preparation_tiers_temps = round(float(temps_preparation) * (4./3.)) 
                        temps_passage_tiers_temps = round(float(temps_passage) * (4./3.))
                        output_matiere = main_database.add_matiere(name, output[1]['id_serie'], temps_preparation, temps_preparation_tiers_temps, temps_passage, temps_passage_tiers_temps, loge, ret=True)
                        try:
                            if output_matiere[0][1] == "success":
                                matieres.append(output_matiere[1])
                        except IndexError:
                            pass
                except IndexError:
                    pass
        

    
    # matieres
    matiere_type = ['Générale', 'Technologique']
    
    for i in tqdm (range (len(series)), desc="Uploading 'Matieres'"):
        output = [['', 'danger']]
        output_salle = [['', 'danger']]
        y = 0
        while output[0][1] == 'danger':
            serie = series[i]
            all_names_possible = []
            if serie["nom"] == "Générale":
                all_names_possible.append(serie["specialite1"])
                all_names_possible.append(serie["specialite2"])
            else:
                if serie["specialite1"] == "STI2D":
                    all_names_possible.append("2I2D")
                elif serie["specialite1"] == "STMG":
                    all_names_possible.append("SGN")
                all_names_possible.append("Mathématiques/Physique")
            for name in all_names_possible:
                if name == "SI" or name == "2I2D":
                    temps_preparation = 60
                    temps_passage = 30
                    if not y:
                        y += 1
                        n = 0
                        while output_salle[0][1] == 'danger':
                            salle = f'D1{n:02d}'
                            output_salle = main_database.add_salle(salle, ret=True)
                            n += 1
                        loge = output_salle[1]["id_salle"]
                    else:
                        loge = output_salle[1]["id_salle"]
                else:
                    temps_preparation = 30
                    temps_passage = 30
                    loge = None
                temps_preparation_tiers_temps = round(float(temps_preparation) * (4./3.)) 
                temps_passage_tiers_temps = round(float(temps_passage) * (4./3.))
                output = main_database.add_matiere(name, serie["id_serie"], temps_preparation, temps_preparation_tiers_temps, temps_passage, temps_passage_tiers_temps, loge, ret=True)
                try:
                    if output[0][1] == "success":
                        matieres.append(output[1])
                except IndexError:
                    pass
                
    # salle
    salles = []
    for i in tqdm (range (len(matieres)), desc="Uploading 'Salles'"):
        output = [['', 'danger']]
        while output[0][1] == 'danger':
            salle = f'D{i:03d}'
            output = main_database.add_salle(salle, ret=True)
            try:
                if output[0][1] == "success":
                    salles.append(output[1])
            except IndexError:
                pass
    
    # professeur
    professeurs = []
    for i in tqdm (range (len(matieres)), desc="Uploading 'Professeurs'"):
        output = [['', 'danger']]
        while output[0][1] == 'danger':
            email = faker.free_email()
            nom = faker.first_name()
            prenom = faker.last_name()
            salle = salles[i]
            output = main_database.add_professeur(email, nom, prenom, salle["id_salle"], ret=True)
            try:
                if output[0][1] == "success":
                    professeurs.append(output[1])
            except IndexError:
                pass
    
    # liste_matiere
    for i in tqdm (range (len(matieres)), desc="Uploading 'Listes Matieres'"):
        output = [['', 'danger']]
        while output[0][1] == 'danger':
            matiere = matieres[i]
            professeur = professeurs[i]
            if matiere['nom'] == "Mathématiques/Physique":
                email = faker.free_email()
                nom = faker.first_name()
                prenom = faker.last_name()
                salle = professeur["salle"]
                ghost_prof = main_database.add_professeur(email, nom, prenom, salle, ret=True)
                main_database.add_liste_matiere(ghost_prof[1]['id_professeur'], matiere['id_matiere'])
            output = main_database.add_liste_matiere(professeur['id_professeur'], matiere['id_matiere'])
    
    # candidat
    for i in tqdm (range (random.randint(3 * len(series), 6 * len(series))), desc="Uploading 'Candidats'"):
        output = ['', '', 'danger']
        while output[2] == 'danger':
            nom = faker.first_name()
            prenom = faker.last_name()
            serie = series[random.randint(0, len(series)-1)]["id_serie"]
            output = main_database.add_candidat(nom, prenom, serie, str(not bool(random.randint(0,7))), False, output=True)
            try:
                # choix_matiere
                candidat = output[0]
                output_candidat = ['', 'danger']
                while output_candidat[1] == 'danger':
                    nom = faker.first_name()
                    prenom = faker.last_name()
                    subjects_available = []
                    for matiere in matieres:
                        # print(matiere["id_serie"], serie)
                        if matiere["id_serie"] == serie:
                            subjects_available.append(matiere["id_matiere"])
                    if subjects_available:
                        subjects_choices = faker.words(2, subjects_available, True)
                        output_candidat = main_database.add_choix_matiere(candidat["id_candidat"], subjects_choices[0], subjects_choices[1]) 
            except IndexError:
                pass