from website.function import main_database

##serie
main_database.add_serie('Generale', 'mathématiques', 'svt')
##salle
main_database.add_salle('D302') 
##matieres
main_database.add_matiere('mathématiques', 1, 30, 40, 50, 60, 1)
##professeur
main_database.add_professeur('prof2@gmail.com', 'mdp', 'Bernard', 'Moquette', 1, 1)
print ("AJOUT FAIS DANS LA BASE")

main_database.delete_account(13)
print ("utilisateur supprimé")