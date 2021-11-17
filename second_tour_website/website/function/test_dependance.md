# TEST DEPENDANCES

## TABLE **SERIE**

### # Insertion 
```python
main_database.add_serie('Generale', 'mathématiques', 'svt')
print ("serie créée")

main_database.add_salle('D302')
print ("salle créée")

main_database.add_matiere('mathématiques', 1, 30, 40, 50, 60, 'D302')
print ("matiere créée")

main_database.add_candidat('matthéo', 'fesneau', 1 , False, output=False)
print ("candidat crée")
```
### # Résultat de l'insertion 

- Table SERIE
  
| id_serie |    nom   |  specialite1  | specialite2 |   
|:--------:|:--------:|:-------------:|:-----------:|
| 1        | Generale | mathématiques | svt         | 

- Table SALLE
  
| id_salle | numero |
|:--------:|:------:|
| 1        | D302   |

- Table MATIERES
  
| id_matiere | id_serie |      nom      |            nom_complet            | temps_preparation | temps_preparation_tiers_temps | temps_passage | temps_passage_tiers_temps | loge |
|:----------:|:--------:|:-------------:|:---------------------------------:|:-----------------:|:-----------------------------:|:-------------:|:-------------------------:|:----:|
| 1          | 1        | mathématiques | mathématiques - mathématiques/svt | 30                | 40                            | 50            | 60                        | D302 |

- Table CANDIDATS
  
| id_candidat |   nom   |  prenom | id_serie | tiers_temps |  
|:-----------:|:-------:|:-------:|:--------:|:-----------:|
| 1           | matthéo | fesneau | 1        | 0           |  


### # Supprimer la serie id=1

```python
main_database.delete_serie(1)
print ("matière supprimée")
```

### # Résultat après la suppression

- Table SERIE : **table vide**
  
- Table SALLE
  
| id_salle | numero |
|:--------:|:------:|
| 1        | D302   |

- Table MATIERES : **table vide**
  
- Table CANDIDATS : **table vide**

<br>

<span style="color:green"><font size = 5> **-- Dépendances Validées --** </font></span>

<br><br>

## TABLE **CANDIDATS**

### # Insertion 
```python
##serie
main_database.add_serie('Generale', 'mathématiques', 'svt')
##salle
main_database.add_salle('D302')
main_database.add_salle('D201')
##matieres
main_database.add_matiere('mathématiques', 1, 30, 40, 50, 60, 'D302')
main_database.add_matiere('svt', 1, 30, 40, 50, 60, 'D201')
##candidats
main_database.add_candidat('matthéo', 'fesneau', 1 , False, output=False)
##choix_matiere
main_database.add_choix_matiere(1, 1, 2)
##creneau
main_database.add_creneau(1, 1, 1, '09:00', '09:10', '09:30')
```
### # Résultat de l'insertion 

- Table SERIE
  
| id_serie |    nom   |  specialite1  | specialite2 |   
|:--------:|:--------:|:-------------:|:-----------:|
| 1        | Generale | mathématiques | svt         | 

- Table SALLE
  
| id_salle | numero |
|:--------:|:------:|
| 1        | D302   |
| 2        | D201   |

- Table MATIERES
  
| id_matiere | id_serie |      nom      |            nom_complet            | temps_preparation | temps_preparation_tiers_temps | temps_passage | temps_passage_tiers_temps | loge |
|:----------:|:--------:|:-------------:|:---------------------------------:|:-----------------:|:-----------------------------:|:-------------:|:-------------------------:|:----:|
| 1          | 1        | mathématiques | mathématiques - mathématiques/svt | 30                | 40                            | 50            | 60                        | D302 |
| 2          | 1        | svt           | svt - mathématiques/svt           | 30                | 40                            | 50            | 60                        | D201 |
|            |          |               |                                   |                   |                               |               |                           |      |

- Table CANDIDATS
  
| id_candidat |   nom   |  prenom | id_serie | tiers_temps |  
|:-----------:|:-------:|:-------:|:--------:|:-----------:|
| 1           | matthéo | fesneau | 1        | 0           |  

- Table CHOIX_MATIERE

| id_choix_matiere | id_candidat | matiere1 | matiere2 |  
|:----------------:|:-----------:|:--------:|:--------:|
| 1                | 1           | 1        | 2        | 

- Table CRENEAU

| id_creneau | id_candidat | id_matiere | id_salle | debut_preparation | fin_preparation |  fin  |  
|:----------:|:-----------:|:----------:|:--------:|:-----------------:|:---------------:|:-----:|
| 1          | 1           | 1          | 1        | 09:00             | 09:10           | 09:30 | 

### # Supprimer le candidat id=1

```python
main_database.delete_candidats(1)
print ("candidat supprimé")
```

### # Résultat après la suppression

- Table SERIE
  
| id_serie |    nom   |  specialite1  | specialite2 |   
|:--------:|:--------:|:-------------:|:-----------:|
| 1        | Generale | mathématiques | svt         | 

- Table SALLE
  
| id_salle | numero |
|:--------:|:------:|
| 1        | D302   |
| 2        | D201   |

- Table MATIERES
  
| id_matiere | id_serie |      nom      |            nom_complet            | temps_preparation | temps_preparation_tiers_temps | temps_passage | temps_passage_tiers_temps | loge |
|:----------:|:--------:|:-------------:|:---------------------------------:|:-----------------:|:-----------------------------:|:-------------:|:-------------------------:|:----:|
| 1          | 1        | mathématiques | mathématiques - mathématiques/svt | 30                | 40                            | 50            | 60                        | D302 |
| 2          | 1        | svt           | svt - mathématiques/svt           | 30                | 40                            | 50            | 60                        | D201 |
|            |          |               |                                   |                   |                               |               |                           |      |

- Table CANDIDATS : **table vide**

- Table CHOIX_MATIERE : **table vide**

- Table CRENEAU : **table vide**

<br>

<span style="color:green"><font size = 5> **-- Dépendances Validées --** </font></span>

<br><br>

## TABLE **SALLE**

### # Insertion 
```python
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
```

### # Résultat de l'insertion 

- Table SERIE
  
| id_serie |    nom   |  specialite1  | specialite2 |   
|:--------:|:--------:|:-------------:|:-----------:|
| 1        | Generale | mathématiques | svt         | 

- Table SALLE
  
| id_salle | numero |
|:--------:|:------:|
| 1        | D302   |

- Table MATIERES
  
| id_matiere | id_serie |      nom      |            nom_complet            | temps_preparation | temps_preparation_tiers_temps | temps_passage | temps_passage_tiers_temps | loge |
|:----------:|:--------:|:-------------:|:---------------------------------:|:-----------------:|:-----------------------------:|:-------------:|:-------------------------:|:----:|
| 1          | 1        | mathématiques | mathématiques - mathématiques/svt | 30                | 40                            | 50            | 60                        | D302 |

- Table CANDIDATS
  
| id_candidat |   nom   |  prenom | id_serie | tiers_temps |  
|:-----------:|:-------:|:-------:|:--------:|:-----------:|
| 1           | matthéo | fesneau | 1        | 0           | 

- Table CRENEAU

| id_creneau | id_candidat | id_matiere | id_salle | debut_preparation | fin_preparation |  fin  |  
|:----------:|:-----------:|:----------:|:--------:|:-----------------:|:---------------:|:-----:|
| 1          | 1           | 1          | 1        | 09:00             | 09:10           | 09:30 | 

- Table PROFESSEUR

| id_professeur | id_utilisateur |   nom   |  prenom  | matiere | salle | 
|:-------------:|:--------------:|:-------:|:--------:|:-------:|:-----:|
| 1             | 11             | Bernard | Moquette | 1       | D302  |

- Table UTILISATEUR

| id |         email        |                        password                                                     | admin |
|:--:|:--------------------:|:-----------------------------------------------------------------------------------:|:-----:|
| 11 | prof@gmail.com       | �֙Dz�#�hOĒ�����=�44e0e,���dĶ����V[��� �5�%�v�c>iC�2%=� | 0     |

### # Supprimer la salle id=1

```python
main_database.delete_salle(1)
print ("salle supprimée")
```

### # Résultat après la suppression

- Table SERIE
  
| id_serie |    nom   |  specialite1  | specialite2 |   
|:--------:|:--------:|:-------------:|:-----------:|
| 1        | Generale | mathématiques | svt         | 

- Table SALLE : **table vide**

- Table MATIERES : **table vide**

- Table CANDIDATS 
  
| id_candidat |   nom   |  prenom | id_serie | tiers_temps |  
|:-----------:|:-------:|:-------:|:--------:|:-----------:|
| 1           | matthéo | fesneau | 1        | 0           |  

- Table CRENEAU : **table vide**

- Table PROFESSEUR : **table vide**

- Table UTILISATEUR

| id |         email        |                        password                                                     | admin |
|:--:|:--------------------:|:-----------------------------------------------------------------------------------:|:-----:|
| 11 | prof@gmail.com       | �֙Dz�#�hOĒ�����=�44e0e,���dĶ����V[��� �5�%�v�c>iC�2%=� | 0     |

<br>

<span style="color:green"><font size = 5> **-- Dépendances Validées --** </font></span>

<br><br>

## TABLE **MATIERES**

### # Insertion 
```python
##serie
main_database.add_serie('Generale', 'mathématiques', 'svt')
##salle
main_database.add_salle('D302')
main_database.add_salle('D201')
##matieres
main_database.add_matiere('mathématiques', 1, 30, 40, 50, 60, 'D302')
main_database.add_matiere('svt', 1, 30, 40, 50, 60, 'D201')
##candidats
main_database.add_candidat('matthéo', 'fesneau', 1 , False, output=False)
##choix_matiere
main_database.add_choix_matiere(1, 1, 2)
##creneau
main_database.add_creneau(1, 1, 1, '09:00', '09:10', '09:30')
##professeur
main_database.add_professeur('prof@gmail.com', 'mdp', 'Bernard', 'Moquette', 1, 'D302')
```

### # Résultat de l'insertion 

- Table SERIE
  
| id_serie |    nom   |  specialite1  | specialite2 |   
|:--------:|:--------:|:-------------:|:-----------:|
| 1        | Generale | mathématiques | svt         | 

- Table SALLE
  
| id_salle | numero |
|:--------:|:------:|
| 1        | D302   |
| 2        | D201   |
  
- Table MATIERES
  
| id_matiere | id_serie |      nom      |            nom_complet            | temps_preparation | temps_preparation_tiers_temps | temps_passage | temps_passage_tiers_temps | loge |
|:----------:|:--------:|:-------------:|:---------------------------------:|:-----------------:|:-----------------------------:|:-------------:|:-------------------------:|:----:|
| 1          | 1        | svt           | svt - mathématiques/svt           | 30                | 40                            | 50            | 60                        | D201 |
|            |          |               |                                   |                   |                               |               |                           |      |


- Table CANDIDATS
  
| id_candidat |   nom   |  prenom | id_serie | tiers_temps |  
|:-----------:|:-------:|:-------:|:--------:|:-----------:|
| 1           | matthéo | fesneau | 1        | 0           |  

- Table CHOIX_MATIERE

| id_choix_matiere | id_candidat | matiere1 | matiere2 |  
|:----------------:|:-----------:|:--------:|:--------:|
| 1                | 1           | 1        | 2        | 

- Table CRENEAU

| id_creneau | id_candidat | id_matiere | id_salle | debut_preparation | fin_preparation |  fin  |  
|:----------:|:-----------:|:----------:|:--------:|:-----------------:|:---------------:|:-----:|
| 1          | 1           | 1          | 1        | 09:00             | 09:10           | 09:30 | 

- Table PROFESSEUR

| id_professeur | id_utilisateur |   nom   |  prenom  | matiere | salle | 
|:-------------:|:--------------:|:-------:|:--------:|:-------:|:-----:|
| 1             | 11             | Bernard | Moquette | 1       | D302  |

- Table UTILISATEUR : **table vide**

### # Supprimer la matière id=1

```python
main_database.delete_matiere(1)
print ("matiere supprimée")
```

### # Résultat après la suppression

- Table SERIE
  
| id_serie |    nom   |  specialite1  | specialite2 |   
|:--------:|:--------:|:-------------:|:-----------:|
| 1        | Generale | mathématiques | svt         | 

- Table SALLE : 

| id_salle | numero |
|:--------:|:------:|
| 1        | D302   |
| 2        | D201   |

- Table MATIERES : 

| id_matiere | id_serie |      nom      |            nom_complet            | temps_preparation | temps_preparation_tiers_temps | temps_passage | temps_passage_tiers_temps | loge |
|:----------:|:--------:|:-------------:|:---------------------------------:|:-----------------:|:-----------------------------:|:-------------:|:-------------------------:|:----:|
| 2          | 1        | svt           | svt - mathématiques/svt           | 30                | 40                            | 50            | 60                        | D201 |
|            |          |               |                                   |                   |                               |               |                           |      |

- Table CANDIDATS 
  
| id_candidat |   nom   |  prenom | id_serie | tiers_temps |  
|:-----------:|:-------:|:-------:|:--------:|:-----------:|
| 1           | matthéo | fesneau | 1        | 0           |  

- Table CHOIX_MATIERE : : **table vide**

- Table CRENEAU : **table vide**

- Table PROFESSEUR : **table vide**

- Table UTILISATEUR : **table vide**

<br>

<span style="color:green"><font size = 5> **-- Dépendances Validées --** </font></span>

<br><br>

## TABLE **PROFESSEUR**

### # Insertion 
```python
##serie
main_database.add_serie('Generale', 'mathématiques', 'svt')
##salle
main_database.add_salle('D302')
##matieres
main_database.add_matiere('mathématiques', 1, 30, 40, 50, 60, 'D302')
##professeur
main_database.add_professeur('prof@gmail.com', 'mdp', 'Bernard', 'Moquette', 1, 'D302')
```

### # Résultat de l'insertion 

- Table SERIE
  
| id_serie |    nom   |  specialite1  | specialite2 |   
|:--------:|:--------:|:-------------:|:-----------:|
| 1        | Generale | mathématiques | svt         | 

- Table SALLE
  
| id_salle | numero |
|:--------:|:------:|
| 1        | D302   |
  
- Table MATIERES
  
| id_matiere | id_serie |      nom      |            nom_complet            | temps_preparation | temps_preparation_tiers_temps | temps_passage | temps_passage_tiers_temps | loge |
|:----------:|:--------:|:-------------:|:---------------------------------:|:-----------------:|:-----------------------------:|:-------------:|:-------------------------:|:----:|
| 1          | 1        | mathématiques | mathématiques - mathématiques/svt | 30                | 40                            | 50            | 60                        | D302 |

- Table PROFESSEUR

| id_professeur | id_utilisateur |   nom   |  prenom  | matiere | salle | 
|:-------------:|:--------------:|:-------:|:--------:|:-------:|:-----:|
| 1             | 11             | Bernard | Moquette | 1       | D302  |

- Table UTILISATEUR : 

| id |         email        |                        password                                                     | admin |
|:--:|:--------------------:|:-----------------------------------------------------------------------------------:|:-----:|
| 11 | prof@gmail.com       | �֙Dz�#�hOĒ�����=�44e0e,���dĶ����V[��� �5�%�v�c>iC�2%=� | 0     |

### # Supprimer la matière id=1

```python
main_database.delete_professeur(1)
print ("professeur supprimé")
```

### # Résultat après la suppression

- Table SERIE
  
| id_serie |    nom   |  specialite1  | specialite2 |   
|:--------:|:--------:|:-------------:|:-----------:|
| 1        | Generale | mathématiques | svt         | 

- Table SALLE : 

| id_salle | numero |
|:--------:|:------:|
| 1        | D302   |

- Table MATIERES : 

| id_matiere | id_serie |      nom      |            nom_complet            | temps_preparation | temps_preparation_tiers_temps | temps_passage | temps_passage_tiers_temps | loge |
|:----------:|:--------:|:-------------:|:---------------------------------:|:-----------------:|:-----------------------------:|:-------------:|:-------------------------:|:----:|
| 1          | 1        | mathématiques | mathématiques - mathématiques/svt | 30                | 40                            | 50            | 60                        | D302 |

- Table PROFESSEUR : **table vide**

- Table UTILISATEUR : **table vide**

<br>

<span style="color:green"><font size = 5> **-- Dépendances Validées --** </font></span>






<br><br>

## TABLE **UTILISATEUR**

### # Insertion 
```python
##serie
main_database.add_serie('Generale', 'mathématiques', 'svt')
##salle
main_database.add_salle('D302')
##matieres
main_database.add_matiere('mathématiques', 1, 30, 40, 50, 60, 'D302')
##professeur
main_database.add_professeur('prof@gmail.com', 'mdp', 'Bernard', 'Moquette', 1, 'D302')
```

### # Résultat de l'insertion 

- Table SERIE
  
| id_serie |    nom   |  specialite1  | specialite2 |   
|:--------:|:--------:|:-------------:|:-----------:|
| 1        | Generale | mathématiques | svt         | 

- Table SALLE
  
| id_salle | numero |
|:--------:|:------:|
| 1        | D302   |
  
- Table MATIERES
  
| id_matiere | id_serie |      nom      |            nom_complet            | temps_preparation | temps_preparation_tiers_temps | temps_passage | temps_passage_tiers_temps | loge |
|:----------:|:--------:|:-------------:|:---------------------------------:|:-----------------:|:-----------------------------:|:-------------:|:-------------------------:|:----:|
| 1          | 1        | mathématiques | mathématiques - mathématiques/svt | 30                | 40                            | 50            | 60                        | D302 |

- Table PROFESSEUR

| id_professeur | id_utilisateur |   nom   |  prenom  | matiere | salle | 
|:-------------:|:--------------:|:-------:|:--------:|:-------:|:-----:|
| 1             | 11             | Bernard | Moquette | 1       | D302  |

- Table UTILISATEUR : 
  
| id |         email        |                        password                                                     | admin |
|:--:|:--------------------:|:-----------------------------------------------------------------------------------:|:-----:|
| 11 | prof@gmail.com       | �֙Dz�#�hOĒ�����=�44e0e,���dĶ����V[��� �5�%�v�c>iC�2%=� | 0     |

### # Supprimer la matière id=1

```python
main_database.delete_account(11)
print ("utilisateur supprimé")
```

### # Résultat après la suppression

- Table SERIE
  
| id_serie |    nom   |  specialite1  | specialite2 |   
|:--------:|:--------:|:-------------:|:-----------:|
| 1        | Generale | mathématiques | svt         | 

- Table SALLE : 

| id_salle | numero |
|:--------:|:------:|
| 1        | D302   |

- Table MATIERES : 

| id_matiere | id_serie |      nom      |            nom_complet            | temps_preparation | temps_preparation_tiers_temps | temps_passage | temps_passage_tiers_temps | loge |
|:----------:|:--------:|:-------------:|:---------------------------------:|:-----------------:|:-----------------------------:|:-------------:|:-------------------------:|:----:|
| 1          | 1        | mathématiques | mathématiques - mathématiques/svt | 30                | 40                            | 50            | 60                        | D302 |

- Table PROFESSEUR : **table vide**

- Table UTILISATEUR : **table vide**

<br>

<span style="color:green"><font size = 5> **-- Dépendances Validées --** </font></span>
