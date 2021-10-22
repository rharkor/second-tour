# Résumé de la premiere interview
## Sujet global
Les élèves participants au second tour sont ceux qui auront eu entre 8 et 10 au BAC.
Notre but seras de créer une interface web à la fois pour les élèves, les professeurs et l'admin (Jean michel giraud : jean-michel.giraud@ac-poitiers.fr).
L'application web seras un calendrier permettant de visualiser à quel heure et ou auront cours les candidats.
Elle permettras aussi de simplifier le travail de monsieur Giraud qui n'auras qu'à rentrer un certain nombre de paramètre pour que le planning se fasse tout seul et de façon optimisé.

## Déroulé d'une année type
### Avant le jour J
L'admin va rentrer en paramètres:
 - le nom des candidats, sa série (+ spécialisations si série = général)
 - Les proffesseurs associé à chaque matière et leur salle
 - L'heure de début
tous les paramètres rentrés précedemment peuvent être modifiable à tout moment. Même une fois les épreuves comméncées !

### Jour J
Dès le matin les élèves irons se présenter à l'admin avec leurs choix de matières, c'est l'admin qui se chargeras de les ajouter sur l'application. Le candidat donneras son nom et les deux matières choisies.

## Spécifications supplémentaires / techniques
 - Les proffesseurs doivent manger entre 13h et 14h il faut donc leur prévoir une pause.
 - Le planning se génère manuellement quand l'admin cliques sur le bouton, à savoir qu'une fois l'heure de début dépassé on ne pourras modifier les heures de passage de chaque élève qu'individuellement.
 - Pour prévoir les retards tous les 5 crénauds un crénaud est vide.
 - Les matières 2I2D et SI sont spéciale, en effet les préparations se font dans une salles prévus pour, elles durent 1h et 30minutes de passage à l'oral, à savoir que la salle de passage n'est pas indiqué c'est un surveillant qui viendras chercher l'élève.
 - Les candidats de la série STI2D passe le premier jour.
 - On ne mélange pas les candidats de série différentes.
 - Les matières Math et Physique des STI2D sont regroupés en une (1 salle / 2 profs / 1 élève).
 - Les matières sont à chercher sur internet (Français et Philosophie sont invluse de base). Pour les STI2D c'est : 
   - Math / Physique
   - 2I2D
   - Philo
   - Français
    Pour les S c'est :
   - Philo
   - Français
   - Spécialité1
   - Spécialité2
 - Les noms des proffesseurs assigné aux élèves ne sont visible que par l'administrateur.
 - Il faudras générer des feuille d'émargement pour chaque prof/salle avec comme info : 

    | Nom du candidat | Heure de début de la préparation | Heure de début de passage | Heure de fin | Emargement     |  
    | :-------------- | :------------------------------: | :-----------------------: | :----------: | -------------: |  
    | NOMCANDIDAT1    | 8h00                             | 8h30                      | 9h00         | ...            | 
    | NOMCANDIDAT2    | 8h30                             | 9h00                      | 9h30         | ...            |  

 - La loge est considérée comme une salle à par entière et auras donc sa propre feuille d'émargement.
 - L'accès au compte admin se feras grâce à un système d'identifiants (nom d'utilisateur, mot de passe).
 - Le calendrier seras accessible de partout sans besoin de compte, il pourras aussi être imprimable.
 - Le fichier excel fournis avant le jour J devras respecter le format suivant : 
    | Nom du candidat | Série   | Spécialisation |
    | :-------------- | :-----: | -------------: |
    | NOMCANDIDAT1    | STI2D   |                |
    | NOMCANDIDAT2    | S       | SI             |
    | NOMCANDIDAT2    | S       | SVT            |