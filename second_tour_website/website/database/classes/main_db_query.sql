create table if not exists salle
(
    id_salle int auto_increment
        primary key,
    numero   varchar(50) not null,
    constraint UNQ_NUMERO
        unique (numero)
);

create table if not exists professeur
(
    id_professeur int auto_increment
        primary key,
    nom           varchar(30) not null,
    prenom        varchar(30) not null,
    salle         int         null,
    constraint fk_professeur__salle_salle foreign key (salle) references salle(id_salle)
);

create table if not exists serie
(
    id_serie    int auto_increment
        primary key,
    nom         varchar(40) not null,
    specialite1 varchar(50) not null,
    specialite2 varchar(50) null,
    constraint UNQ_NOM_SPE1_SPE2
        unique (nom, specialite1, specialite2),
);

create table if not exists candidat
(
    id_candidat int auto_increment
        primary key,
    nom         varchar(200) not null,
    prenom      varchar(150) not null,
    id_serie    int          not null,
    tiers_temps tinyint(1)   not null,
    absent      tinyint(1)   not null,
    constraint fk_candidat_id_serie_serie foreign key (id_serie) references serie(id_serie)
);

create table if not exists matiere
(
    id_matiere                    int auto_increment
        primary key,
    id_serie                      int         not null,
    nom                           varchar(30) not null,
    nom_complet                   varchar(60) not null,
    temps_preparation             int         not null,
    temps_preparation_tiers_temps int         not null,
    temps_passage                 int         not null,
    temps_passage_tiers_temps     int         not null,
    loge                          int         null,
    constraint UNQ_NOM_NOMCOMP_TPS_PREPA
        unique (nom, nom_complet, temps_preparation, temps_passage),

    constraint fk_matiere_serie foreign key (id_serie) references serie(id_serie),
    constraint fk_matiere_salle foreign key (loge) references salle(id_salle)
);

create table if not exists choix_matiere
(
    id_choix_matiere int auto_increment
        primary key,
    id_candidat      int not null,
    matiere1         int null,
    matiere2         int null,
    constraint UNQ_CANDIDAT
        unique (id_candidat),
    constraint fk_choix_matiere_matiere1 foreign key (matiere1) references matiere(id_matiere),
    constraint fk_choix_matiere_matiere2 foreign key (matiere2) references matiere(id_matiere),
    constraint fk_choix_matiere_id_candidat foreign key (id_candidat) references candidat(id_candidat)
);

create table if not exists creneau
(
    id_creneau        int auto_increment
        primary key,
    id_candidat       int      not null,
    id_matiere        int      not null,
    id_salle          int      not null,
    debut_preparation datetime not null,
    fin_preparation   datetime not null,
    fin               datetime not null,
    constraint UNQ_CANDIDAT_MATIERE
        unique (id_candidat, id_matiere),
    constraint UNQ_CANDIDAT_PREPA
        unique (id_candidat, debut_preparation),
    constraint fk_creneau_id_candidat foreign key (id_candidat) references candidat(id_candidat),
    constraint fk_creneau_id_matiere foreign key (id_matiere) references matiere(id_matiere),
    constraint fk_creneau_id_salle foreign key (id_salle) references salle(id_salle)
);

create table if not exists horaire
(
    id_horaire   int auto_increment
        primary key,
    horaire_arr1  datetime not null,
    horaire_dep1  datetime not null,
    horaire_arr2  datetime not null,
    horaire_dep2  datetime not null,
    horaire_arr3  datetime not null,
    horaire_dep3  datetime not null,
    id_professeur int      not null,
    constraint fk_horraire_id_professeur foreign key (id_professeur) references professeur(id_professeur)
);

create table if not exists liste_matiere
(
    id_liste_matiere int auto_increment
        primary key,
    id_professeur    int not null,
    id_matiere       int not null,
    constraint UNQ_PROFESSEUR_MATIERE
        unique (id_professeur, id_matiere),
    constraint fk_liste_matiere_id_professeur foreign key (id_professeur) references professeur(id_professeur),
    constraint fk_liste_matiere_id_matiere foreign key (id_matiere) references matiere(id_matiere)
);

create table if not exists token
(
    id_token            int auto_increment
        primary key,
    email         varchar(200) not null,
    token         varchar(200) not null,
    id_professeur int          null,
    admin         boolean   not null,
    constraint unique_token
        unique (token),
    constraint fk_token_id_professeur foreign key (id_professeur) references professeur(id_professeur)
);

create table if not exists utilisateur
(
    id_utilisateur            int auto_increment
        primary key,
    email         varchar(200) not null,
    password      varchar(200) not null,
    admin         tinyint(1)   not null,
    id_professeur int          null,
    constraint UNQ_utilisateur_email
        unique (email, admin),
    constraint fk_utilisateur_id_professeur foreign key (id_professeur) references professeur(id_professeur)
);

create index id_serie
    on candidat (id_serie);

create index matiere1
    on choix_matiere (matiere1);

create index matiere2
    on choix_matiere (matiere2);

create index id_matiere
    on creneau (id_matiere);

create index id_salle
    on creneau (id_salle);

create index id_matiere
    on liste_matiere (id_matiere);

create index id_serie
    on matiere (id_serie);

create index salle
    on professeur (salle);

create index id_professeur
    on token (id_professeur);

create index id_professeur
    on utilisateur (id_professeur);

insert into utilisateur
values (1,'admin@ac-poitiers.fr','$p5k2$3e8$AfpOzesj$.KoGR.raCRkA3gne.aZrF1bQobRfdSIH',1,NULL);
