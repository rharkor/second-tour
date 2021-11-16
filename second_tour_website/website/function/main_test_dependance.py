from website.function import main_database

##serie
main_database.add_serie('Generale', 'mathématiques', 'svt')
##salle
main_database.add_salle('D302')
##matieres
main_database.add_matiere('mathématiques', 1, 30, 40, 50, 60, 'D302')
##candidats
main_database.add_candidat('matthéo', 'fesneau', 1 , False, output=False)
##creneau
main_database.add_creneau(1, 1, 1, '09:00', '09:10', '09:30')
##professeur
main_database.add_professeur('prof@gmail.com', 'mdp', 'Bernard', 'Moquette', 1, 'D302')
print ("AJOUT FAIS DANS LA BASE")
##main_database.delete_salle(1)
##print ("salle supprimée")