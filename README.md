- Vers notre [Miro](https://miro.com/app/board/o9J_lq-Az28=/) <br>
- Vers notre [Figma](https://www.figma.com/file/9ZiTvUc1RZmHgXqwQZ7R7n/Untitled?node-id=0%3A1)

#### Lancer le projet:
Pour lancer le projet il faut lancer la stack docker.

Se placer dans la stack:
```console
cd stack
```

Lancer la stack:
```console
docker-compose up --build
```

Pour lancer le visualisateur des échanges réseaux, il faut :
 - Vérifier que "NETWORK_VISU=true" dans les .env de l'api et du site internet
 - LOCAL_IP=.... soit bien l'adresse ip de la machine en question (toujours dans les mêmes .env)
 - Lancer le `NetworkExchangeVisualisation` à l'aide de la commande `node app.js` avant la stack docker

Pour accéder aux conteneurs individuels il faut éxecuter (*la stack doit être entrain de tourner*):
```console
docker exec -it nom-du-conteneur bash
```

*ps: Le site et l'API ont un fichier de log accessible à leur racine.*

#### Lancer les tests:
Il faut dans un premier temps se placer dans le répertoire `tests`.   
Pour executer les tests unitaires :    
`npm run test`    

Pour executer les tests fonctionnels :   
`npm run test:ui`   
*ps: Les test fonctionnels prennent un peu de temps à se lancer*   


#### Execution des fixtures:
Afin de lancer les fixtures il faut executer la commande `python tests.py` dans le répertoire ***stack\website\secondtour_website***


#### Différents partis du projet:

- Élèves : HUORT Louis / HACALA Maude / DESCROIX Max / FESNEAU Matthéo / SANTAGUILIANA Théau
- Clients : SPITERI Patrick, proviseur adjoint du Lycée Vieljeux de La Rochelle ainsi que GIRAUD Jean-Michel qui a suivi le projet durant son déroulement.
- Tuteur : MALKI Jamal
- Planification du passage des candidats au second groupe d'épreuves du Baccalauréat (Oraux de rattrapage)
seconde année de DUT Informatique promotion 2022

#### Présentation du sujet:

##### Contexte :
Le Lycée Vieljeux de La Rochelle (Lycée général et technologique) à fait appel aux étudiants du DUT informatique de La Rochelle afin qu’ils puissent leur apporter une application permettant de générer automatiquement le planning des rattrapages du BAC. Pour rappel, un candidat du baccalauréat est amené à participer aux oraux de rattrapage lorsqu’il termine les épreuves du baccalauréat avec une moyenne située entre 8 et 10 sur 20. Le jour même de son rattrapage, l’élève choisit deux matières parmi celles qui ont fait l'objet d'épreuves écrites lors des épreuves du baccalauréat (Philosophie, Français, ses deux spécialités).

##### Objectifs :
L'objectif du projet est de créer une application permettant de proposer à l'affichage un planning de passage pour chaque candidat admis au second groupe d'épreuves(rattrapage). Ce planning devra, en fonction des choix des candidats et des capacités du centre d'examen, mentionner les horaires de passage ainsi que la salle d'interrogation.

##### Enjeux :
Il faut que l’application soit fonctionnelle avant les épreuves du baccalauréat 2022 (Avant juin 2022) afin qu'elle puisse être utilisée pour celles-ci.

#### 1. [Présentation du projet](https://github.com/rharkor/second-tour/wiki/Pr%C3%A9sentation-du-projet)

- [Sujet de base](https://github.com/rharkor/second-tour/wiki/Pr%C3%A9sentation-du-projet#sujet-de-base)
- [Notre équipe](https://github.com/rharkor/second-tour/wiki/Pr%C3%A9sentation-du-projet#notre-%C3%A9quipe)
- [Logiciels/Applications utilisées](https://github.com/rharkor/second-tour/wiki/Pr%C3%A9sentation-du-projet#logicielsapplications-utilis%C3%A9es)
- [Langage de programmation utiliser](https://github.com/rharkor/second-tour/wiki/Pr%C3%A9sentation-du-projet#langage-de-programmation-utiliser)
- [Framework utilisé](https://github.com/rharkor/second-tour/wiki/Pr%C3%A9sentation-du-projet#framework-utilis%C3%A9)
- [Schéma des relations avec l'API](https://github.com/rharkor/second-tour/wiki/Pr%C3%A9sentation-du-projet#sch%C3%A9ma-des-relations-avec-lapi)

#### 2. [Charte graphique](https://github.com/rharkor/second-tour/wiki/Charte-graphique)

- [Logo](https://github.com/rharkor/second-tour/wiki/Charte-graphique#1-logo)
- [Couleurs utilisées](https://github.com/rharkor/second-tour/wiki/Charte-graphique#2-couleurs-utilisees)
- [Typographie](https://github.com/rharkor/second-tour/wiki/Charte-graphique#3-typographie)
- [Illustration et banque d'images](https://github.com/rharkor/second-tour/wiki/Charte-graphique#4-illustrations-et-banque-dimages)



#### 3. [Navigation](https://github.com/rharkor/second-tour/wiki/Navigation)
- [Pages accessible à tous](https://github.com/rharkor/second-tour/wiki/Navigation#pages-accessible-%C3%A0-tous)
- [Page professeur](https://github.com/rharkor/second-tour/wiki/Navigation#page-professeur)
- [Pages administrateur](https://github.com/rharkor/second-tour/wiki/Navigation#pages-administrateur)


#### 4. [Base de données](https://github.com/rharkor/second-tour/wiki/Base-de-données)

- [Dictionnaire des relations](https://github.com/rharkor/second-tour/wiki/Base-de-donn%C3%A9es#1-dictionnaire-des-relations)
- [Schéma des relations](https://github.com/rharkor/second-tour/wiki/Base-de-donn%C3%A9es#2-schema-des-relations)
- [Dictionnaire des attributs](https://github.com/rharkor/second-tour/wiki/Base-de-donn%C3%A9es#3-dictionnaire-des-attributs-des-relations-de-la-base-de-donnees)
- [Schéma](https://github.com/rharkor/second-tour/wiki/Base-de-donn%C3%A9es#4-schema-de-la-base-de-donnees)



#### 5. [Documentation Flask](https://github.com/rharkor/second-tour/wiki/Documentation-Flask)

- [Présentation de Flask](https://github.com/rharkor/second-tour/wiki/Documentation-Flask#1-pr%C3%A9sentation-de-flask)
- [Débuter un projet avec le framework Flask](https://github.com/rharkor/second-tour/wiki/Documentation-Flask#2-d%C3%A9buter-un-projet-avec-le-framework-flask)
- [Installation du framework Flask](https://github.com/rharkor/second-tour/wiki/Documentation-Flask#2-d%C3%A9buter-un-projet-avec-le-framework-flask)
  - [Création de la première page du projet](https://github.com/rharkor/second-tour/wiki/Documentation-Flask#2-creation-de-la-premiere-page-du-projet)
  - [Création des différentes routes](https://github.com/rharkor/second-tour/wiki/Documentation-Flask#3-definition-des-differentes-routes)
  - [Exécuter le projet](https://github.com/rharkor/second-tour/wiki/Documentation-Flask#4-executer-le-projet)  
  - [HTML et Template](https://github.com/rharkor/second-tour/wiki/Documentation-Flask#5-html-et-template)



#### 6. [Réunions avec le client](https://github.com/rharkor/second-tour/wiki/R%C3%A9union-avec-le-client)

- [Réunion du 22 octobre 2021](https://github.com/rharkor/second-tour/wiki/R%C3%A9union-avec-le-client#r%C3%A9sum%C3%A9-de-la-premi%C3%A8re-r%C3%A9union-du-22-octobre-2021)
- [Réunion du 18 novembre 2021](https://github.com/rharkor/second-tour/wiki/R%C3%A9union-avec-le-client#r%C3%A9sum%C3%A9-de-la-seconde-r%C3%A9union-du-18-novembre-2021)
- [Réunion du 4 février 2022](https://github.com/rharkor/second-tour/wiki/R%C3%A9union-avec-le-client#r%C3%A9sum%C3%A9-de-la-troisi%C3%A8me-r%C3%A9union-4-f%C3%A9vrier-2022)


#### 7. [Réunions avec le tuteur](https://github.com/rharkor/second-tour/wiki/R%C3%A9union-avec-le-tuteur)
- [Réunion du 1er décembre 2021](https://github.com/rharkor/second-tour/wiki/R%C3%A9union-avec-le-tuteur#r%C3%A9union-du-1er-d%C3%A9cembre-2021)
- [Réunion du 2 Mars 2022](https://github.com/rharkor/second-tour/wiki/R%C3%A9union-avec-le-tuteur#r%C3%A9union-du-2-mars-2022)

#### 8. [Documentation API](https://github.com/rharkor/second-tour/wiki/Documentation-de-l'API#documentation-de-lapi)
- [Présentation de l'API](https://github.com/rharkor/second-tour/wiki/Documentation-de-l'API#1-pr%C3%A9sentation-de-lapi)
- [Définition des routes](https://github.com/rharkor/second-tour/wiki/Documentation-de-l'API#2-d%C3%A9finition-des-routes)

#### 9. [Gestion de projet](https://github.com/rharkor/second-tour/wiki/Gestion-de-projet#gestion-du-projet)
- [Périmètre du projet](https://github.com/rharkor/second-tour/wiki/Gestion-de-projet#p%C3%A9rim%C3%A8tre-du-projet)
     - [Détails de la vision produit](https://github.com/rharkor/second-tour/wiki/Gestion-de-projet#d%C3%A9tails-de-la-vision-produit)
     - [Les contraintes](https://github.com/rharkor/second-tour/wiki/Gestion-de-projet#les-contraintes)
     - [Les livrables attendus](https://github.com/rharkor/second-tour/wiki/Gestion-de-projet#les-livrables-attendus)
- [Organisation du projet](https://github.com/rharkor/second-tour/wiki/Gestion-de-projet#organisation-du-projet)
     - [Méthodologie de projet](https://github.com/rharkor/second-tour/wiki/Gestion-de-projet#m%C3%A9thodologie-de-projet)
     - [Outils de suivi de projet](https://github.com/rharkor/second-tour/wiki/Gestion-de-projet#outils-de-suivi-de-projet)
     - [Répartition du travail](https://github.com/rharkor/second-tour/wiki/Gestion-de-projet#r%C3%A9partition-du-travail-entre-les-membres-du-groupe)
     - [Organisation](https://github.com/rharkor/second-tour/wiki/Gestion-de-projet#organisation)
     
#### 10. [Projet réalisé](https://github.com/rharkor/second-tour/wiki/Projet-r%C3%A9alis%C3%A9)
- [Fonctionnalités implémentées](https://github.com/rharkor/second-tour/wiki/Projet-r%C3%A9alis%C3%A9#fonctionnalit%C3%A9s-impl%C3%A9ment%C3%A9es)
     - [Partie accueil](https://github.com/rharkor/second-tour/wiki/Projet-r%C3%A9alis%C3%A9#partie-accueil)
     - [Partie admin](https://github.com/rharkor/second-tour/wiki/Projet-r%C3%A9alis%C3%A9#partie-admin)
     - [Partie professeur](https://github.com/rharkor/second-tour/wiki/Projet-r%C3%A9alis%C3%A9#partie-professeur)
- [Rétrospective finale](https://github.com/rharkor/second-tour/wiki/Projet-r%C3%A9alis%C3%A9#r%C3%A9trospective-finale)
     - [Rétrospective individuelle](https://github.com/rharkor/second-tour/wiki/Projet-r%C3%A9alis%C3%A9#r%C3%A9trospective-individuelle)
     - [Rétrospective d'équipe](https://github.com/rharkor/second-tour/wiki/Projet-r%C3%A9alis%C3%A9#r%C3%A9trospective-d%C3%A9quipe)
- [Bilan du projet](https://github.com/rharkor/second-tour/wiki/Projet-r%C3%A9alis%C3%A9#bilan-du-projet)
