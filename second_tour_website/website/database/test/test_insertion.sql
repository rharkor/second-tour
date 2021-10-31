--INSERTION DES SALLES--
INSERT INTO SALLE
VALUES (NULL, 'D100');
INSERT INTO SALLE
VALUES (NULL, 'D101');
INSERT INTO SALLE
VALUES (NULL, 'D003');
INSERT INTO SALLE
VALUES (NULL, 'D004');
INSERT INTO SALLE
VALUES (NULL, 'D005');
INSERT INTO SALLE
VALUES (NULL, 'D006');
INSERT INTO SALLE
VALUES (NULL, 'D007');
INSERT INTO SALLE
VALUES (NULL, 'D008');
INSERT INTO SALLE
VALUES (NULL, 'D009');
INSERT INTO SALLE
VALUES (NULL, 'D010');
INSERT INTO SALLE
VALUES (NULL, 'D011');
INSERT INTO SALLE
VALUES (NULL, 'D012');

--INSERTION DES SERIES--
INSERT INTO SERIE
VALUES (NULL, 'Générale', 'Mathématiques', 'SVT');
INSERT INTO SERIE
VALUES (NULL, 'Générale', 'Physique', 'SI');
INSERT INTO SERIE
VALUES (NULL, 'Technologique', 'STI2D', NULL);

--INSERTION DES MATIERES--
INSERT INTO MATIERES
VALUES (NULL, 1, 'Mathématiques', 'Mathématiques - Mathématiques/SVT', 30, 30, NULL);
INSERT INTO MATIERES
VALUES (NULL, 1, 'SVT', 'SVT - Mathématiques/SVT', 30, 30, NULL);
INSERT INTO MATIERES
VALUES (NULL, 1, 'Français', 'Français - Mathématiques/SVT', 30, 30, NULL);
INSERT INTO MATIERES
VALUES (NULL, 1, 'Philosophie', 'Philosophie - Mathématiques/SVT', 30, 30, NULL);

INSERT INTO MATIERES
VALUES (NULL, 2, 'Physique', 'Physique - Physique/SI', 30, 30, NULL);
INSERT INTO MATIERES
VALUES (NULL, 2, 'SI', 'SI - Physique/SI', 60, 30, 1);
INSERT INTO MATIERES
VALUES (NULL, 2, 'Français', 'Français - Physique/SI', 30, 30, NULL);
INSERT INTO MATIERES
VALUES (NULL, 2, 'Philosophie', 'Philosophie - Physique/SI', 30, 30, NULL);

INSERT INTO MATIERES
VALUES (NULL, 3, '2I2D', '2I2D - STI2D', 60, 30, 2);
INSERT INTO MATIERES
VALUES (NULL, 3, 'Mathématiques/Physique', 'Mathématiques/Physique - STI2D', 30, 30, NULL);
INSERT INTO MATIERES
VALUES (NULL, 3, 'Français', 'Français - STI2D', 30, 30, NULL);
INSERT INTO MATIERES
VALUES (NULL, 3, 'Philosophie', 'Philosophie - STI2D', 30, 30, NULL);

--INSERTION DES CANDIDATS--
INSERT INTO CANDIDATS
VALUES (NULL, 'Oumiri', 'Hakim', 1);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 1, 1, 2);

INSERT INTO CANDIDATS
VALUES (NULL, 'Garland', 'Gamelin', 1);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 2, 1, 3);

INSERT INTO CANDIDATS
VALUES (NULL, 'Huon', 'Guimond', 2);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 3, 5, 6);

INSERT INTO CANDIDATS
VALUES (NULL, 'Pinette', 'Agathe', 3);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 4, 9, 10);

INSERT INTO CANDIDATS
VALUES (NULL, 'Allain', 'Clothilde', 3);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 5, 9, 10);

INSERT INTO CANDIDATS
VALUES (NULL, 'Jalbert', 'Arienne', 3);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 6, 9, 10);

INSERT INTO CANDIDATS
VALUES (NULL, 'Bernard', 'Noémie', 3);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 7, 9, 11);

INSERT INTO CANDIDATS
VALUES (NULL, 'Gousse', 'Maurice', 1);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 8, 1, 3);

INSERT INTO CANDIDATS
VALUES (NULL, 'Le mendes', 'Isaac', 1);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 9, 2, 3);

INSERT INTO CANDIDATS
VALUES (NULL, 'Guillot', 'Henri', 1);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 10, 1, 2);

INSERT INTO CANDIDATS
VALUES (NULL, 'Foucher', 'Charlotte', 2);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 11, 5, 6);

INSERT INTO CANDIDATS
VALUES (NULL, 'Duhamel', 'Claire', 2);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 12, 5, 6);

INSERT INTO CANDIDATS
VALUES (NULL, 'Pons', 'Sebastien', 2);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 13, 5, 6);

INSERT INTO CANDIDATS
VALUES (NULL, 'Vincent', 'Noémie', 2);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 14, 5, 7);

INSERT INTO CANDIDATS
VALUES (NULL, 'Lefebvre', 'Gilles', 3);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 15, 9, 10);

INSERT INTO CANDIDATS
VALUES (NULL, 'Devaux', 'Marine', 3);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 16, 9, 10);

INSERT INTO CANDIDATS
VALUES (NULL, 'Labbe', 'David', 3);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 17, 9, 10);

INSERT INTO CANDIDATS
VALUES (NULL, 'Gomes', 'Aimé', 3);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 18, 9, 10);

INSERT INTO CANDIDATS
VALUES (NULL, 'Ribeiro', 'Alfred', 3);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 19, 9, 10);

INSERT INTO CANDIDATS
VALUES (NULL, 'Romero', 'Julio', 3);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 20, 9, 12);

INSERT INTO CANDIDATS
VALUES (NULL, 'Leroy', 'Benoît', 3);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 21, 10, 11);

INSERT INTO CANDIDATS
VALUES (NULL, 'Dias', 'Gilles', 3);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 22, 10, 11);

INSERT INTO CANDIDATS
VALUES (NULL, 'Lemaire', 'Alain', 3);
INSERT INTO CHOIX_MATIERE
VALUES (NULL, 23, 10, 9);

--INSERTION DES PROFESSEURS--
-- INSERT INTO PROFESSEUR
-- VALUES (NULL, 1, 'Hubert', 'Jean', 1, 2); --PROF WITH ACCOUNT ALREADY MADE MANUALLY
-- MATHS G
INSERT INTO PROFESSEUR
VALUES (NULL, 2, 'De Renaud', 'Julien', 1, 3);
-- SVT G
INSERT INTO PROFESSEUR
VALUES (NULL, 1, 'Pelletier-aubert', 'Aimé', 2, 4);
-- FRANCAIS G
INSERT INTO PROFESSEUR
VALUES (NULL, 1, 'Langlois', 'Marie-Charlotte', 3, 5);
INSERT INTO PROFESSEUR
VALUES (NULL, 1, 'Langlois', 'Marie-Charlotte', 7, 5);
-- PHILO G
INSERT INTO PROFESSEUR
VALUES (NULL, 1, 'Lacroix', 'Daisy', 4, 6);
INSERT INTO PROFESSEUR
VALUES (NULL, 1, 'Lacroix', 'Daisy', 8, 6);
-- PYSIQUE G
INSERT INTO PROFESSEUR
VALUES (NULL, 1, 'Goncalves', 'Denis', 5, 7);
-- SI G
INSERT INTO PROFESSEUR
VALUES (NULL, 1, 'Renault', 'Thomas', 6, 8);
-- 2I2D STI2D
INSERT INTO PROFESSEUR
VALUES (NULL, 1, 'Legendre', 'Rémy', 9, 9);
-- MATHS/PHYSIQUE 2I2D
INSERT INTO PROFESSEUR
VALUES (NULL, 1, 'Adam', 'Paul', 10, 10);
INSERT INTO PROFESSEUR
VALUES (NULL, 1, 'Périer', 'Valérie', 10, 10);
-- FRANCAIS STI2D
INSERT INTO PROFESSEUR
VALUES (NULL, 1, 'Devaux', 'Jacques', 11, 11);
-- PHILO STI2D
INSERT INTO PROFESSEUR
VALUES (NULL, 1, 'Teixera', 'Pénélope', 12, 12);



--GENERATION AUTOMATIQUE APRES--
-- INSERT INTO CRENEAU
-- VALUES (NULL, 1, 1, 2, '09:00', '10:00');
-- INSERT INTO CRENEAU
-- VALUES (NULL, 1, 2, 5, '11:00', '12:00');

-- INSERT INTO CRENEAU
-- VALUES (NULL, 4, 9, 5, '09:00', '10:30');
-- INSERT INTO CRENEAU
-- VALUES (NULL, 4, 10, 4, '11:00', '12:00');