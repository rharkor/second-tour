from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import inspect
from sqlalchemy import create_engine

from website.main_website import app, db, logging
from website.function import main_database
import shutil, os, sqlite3

database = 'second_tour_website\website\database\data.sqlite3'
copie_database = 'second_tour_website\website\database\copie_data.sqlite3'

# Copie le contenu du fichier main_classes.py dans un nouveau fichier 
shutil.copyfile(database, copie_database)

# Supprimer le fichier data.sqlite3
#os.remove(database)

# Créer le fichier 
file = open(database, "w")
file.close()

# Initialiser  le fichier de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.create_all()

# Vérification de la présence des tables de copie_database dans database

con_copie = sqlite3.connect(copie_database)
cursor_copie = con_copie.cursor()
cursor_copie.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor_copie.fetchall())

con_data = sqlite3.connect(database)
cursor_data = con_data.cursor()
cursor_data.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor_data.fetchall())

print(1)
for copie in cursor_copie.fetchall() :

    print(2)
    for data in cursor_data.fetchall() :
    
        if copie == data :
        
            print("la table ", copie," existe")
        
    





