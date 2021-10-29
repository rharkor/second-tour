# DESCRIPTION DE LA BASE DE DONNEES 

## ```1. DICTIONNAIRE DES RELATIONS DE LA BASE DE DONNEES```
<br>

| RELATION      | DESCRIPTION                                                                     |  
|---------------|---------------------------------------------------------------------------------|
| CANDIDATS     | Ensemble des candidats se présentant au second tour                             |
| SERIE         | Ensemble des séries disponibles dans le lycée ( ici générale et technologique ) |
| MATIERES      | Ensemble des matières possible au second tour                                   |
| CHOIX_MATIERE | Choix des 2 matières d'un candidat                                              |
| PROFESSEUR    | Ensemble des professeurs examinteur au second tour                              |
| UTILISATEURS  | Ensemble des utilisateurs pouvant se connecter a l'application web              |
| SALLE         | Ensemble des salles disponibles                                                 |
| CRENEAU       | Ensemble de créneaux disponibles                                                |

<br>

## ```2. SCHEMA DES RELATIONS DE LA BASE DE DONNEES```

<br>

| RELATION      | SCHEMA                                                                         | CLE PRIMAIRE     | CLE UNIQUE                                      |  
|---------------|--------------------------------------------------------------------------------|------------------|-------------------------------------------------|
| CANDIDATS     | ID_CANDIDAT, NOM, PRENOM, ID_SERIE                                             | ID_CANDIDAT      |                                                 |
| SERIE         | ID_SERIE, NOM, SPECIALITE1, SPECIALITE2                                        | ID_SERIE         | NOM, SPECIALITE1, SPECIALITE2                   |
| MATIERES      | ID_MATIERE, ID_SERIE, NOM, NOM_COMPLET, TEMPS_PREPARATION, TEMPS_PASSAGE, LOGE | ID_MATIERE       | NOM, NOM_COMPLET (TEMPS_PREPARATION, TEMPS_PASSAGE) |
| CHOIX_MATIERE | ID_CHOIX_MATIERE, ID_CANDIDAT, MATIERE1, MATIERE2                              | ID_CHOIX_MATIERE | ID_CANDIDAT, ID_MATIERE, DEBUT_PREPARATION      |
| PROFESSEUR    | ID_PROFESSEUR, ID_UTILISATEUR, NOM, PRENOM, MATIERE, SALLE                     | ID_PROFESSEUR    | ID_UTILISATEUR, NOM, PRENOM (MATIERE)           |
| UTILISATEURS  | ID_UTILISATEUR, EMAIL, MOT_DE_PASSE, ADMIN                                     | ID_UTILISATEUR   | EMAIL, ADMIN                                    |
| SALLE         | ID_SALLE, NUMERO                                                               | ID_SALLE         | NUMERO                                          |
| CRENEAU       | ID_CRENEAU, ID_CANDIDAT, ID_MATIERE, ID_SALLE, DEBUT_PREPARATION               | ID_CRENEAU       | ID_CANDIDAT                                     |

<br>

## ```3. DICTIONNAIRE DES ATTRIBUTS DES RELATIONS DE LA BASE DE DONNEES```

<br>

| RELATION      | ATTRIBUT          | TYPE     | TAILLE | O/F | DESCRIPION                                                  |  
|---------------|-------------------|----------|:------:|:---:|-------------------------------------------------------------|
|```CANDIDATS```| ID_CANDIDAT       | INTEGER  |        | O   | Identifiant du candidat                                     |
|               | NOM               | STRING   | 200    | O   | Nom du candidat                                             |
|               | PRENOM            | STRING   | 150    | O   | Prénom du candidat                                          |
|               | ID_SERIE          | INTEGER  |        | O   | Identifiant de la série du candidat                         |
|||||||
|```SERIE```    | ID_SERIE          | INTEGER  |        | O   | Identifiant de la série                                     |
|               | NOM               | STRING   | 40     | O   | Nom de la série (Général ou STI2D)                          |
|               | SPECIALITE1       | STRING   | 50     | O   | Nom de la spécialité                                        |
|               | SPECIALITE2       | STRING   | 50     | F   | Nom de la deuxième spécialité NULL pour les séries STI2D    |
|||||||
|```MATIERES``` | ID_MATIERE        | INTEGER  |        | O   | Identifiant de la matière                                   |
|               | ID_SERIE          | INTEGER  |        | O   | Identifiant de la série auquelle cette matière est associée |
|               | NOM               | STRING   | 30     | O   | Nom de la matière                                           |
|               | NOM_COMPLET       | STRING   | 60     | O   | Nom complet de la matière                                   |
|               | TEMPS_PREPARATION | INTEGER  |        | O   | Temps de préparation à l'épreuve                            |
|               | TEMPS_PASSAGE     | INTEGER  |        | O   | Durée du passage de l'épreuve                               |
|               | LOGE              | INTEGER  |        | F   | Loge associée au passage                                    |
|||||||
|```CHOIX_MATIERE```| ID_CHOIX_MATIERE  | INTEGER  |        | O   | Identifiant du choix des matières du candidat               |
|                   | ID_CANDIDAT       | INTEGER  |        | O   | Identifiant du candidat                                     |
|                   | MATIERE1          | INTEGER  |        | F   | Matière choisie 1                                           |
|                   | MATIERE2          | INTEGER  |        | F   | Matière choisie 2                                           |
|||||||
|```PROFESSEUR```| ID_PROFESSEUR     | INTEGER  |        | O   | Identifiant du professeur                                   |
|                | ID_UTILISATEUR    | INTEGER  |        | O   | Identifiant de l'utilisateur                                |
|                | NOM               | STRING   | 30     | O   | Nom du professeur                                           |
|                | PRENOM            | STRING   | 30     | O   | Prénom du professeur                                        |
|                | MATIERE           | INTEGER  |        | O   | Matière évaluée                                             |
|                | SALLE             | INTEGER  |        | O   | Salle d'examen                                              |
|||||||
|```UTILISATEURS```| ID_UTILISATEUR    | INTEGER  |        | O   | Identifiant de l'utilisateur                                |
|                  | EMAIL             | STRING   | 200    | O   | Adresse mail de l'utilisateur                               |
|                  | MOT_DE_PASSE      | STRING   | 200    | O   | Mot de passe de l'utilisateur                               |
|                  | ADMIN             | BOOL     |        | O   | TRUE si l'utilisateur est un admin, sinon FALSE             |
|||||||
|```SALLE```    | ID_SALLE          | INTEGER  |        | O   | Identifiant de la salle                                     |
|               | NUMERO            | STRING   | 50     | O   | Numéro de la salle                                          |
|||||||
|```CRENEAU```  | ID_CRENEAU        | INTEGER  |        | O   | Identifiant du créneau                                      |
|               | ID_CANDIDAT       | INTEGER  |        | O   | Identifiant du candidat                                     |
|               | ID_MATIERE        | INTEGER  |        | O   | Identifiant de la matière                                   |
|               | ID_SALLE          | INTEGER  |        | O   | Identifiant de la salle                                     |
|               | DEBUT_PREPARATION | DATETIME |        | O   | Heure du début de la préparation                            |

