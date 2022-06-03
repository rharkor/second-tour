-- MySQL dump 10.13  Distrib 8.0.22, for Linux (x86_64)
--
-- Host: localhost    Database: secondtour
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `candidat`
--

DROP TABLE IF EXISTS `candidat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidat` (
  `id_candidat` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(200) NOT NULL,
  `prenom` varchar(150) NOT NULL,
  `id_serie` int NOT NULL,
  `tiers_temps` tinyint(1) NOT NULL,
  `absent` tinyint(1) NOT NULL,
  PRIMARY KEY (`id_candidat`),
  KEY `id_serie` (`id_serie`),
  CONSTRAINT `fk_candidat_id_serie_serie` FOREIGN KEY (`id_serie`) REFERENCES `serie` (`id_serie`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidat`
--

LOCK TABLES `candidat` WRITE;
/*!40000 ALTER TABLE `candidat` DISABLE KEYS */;
INSERT INTO `candidat` VALUES (1,'Dupuis','Eugène',1,0,0),(2,'Heude','Jean',6,1,0),(3,'Huort','Julie',4,0,0),(4,'Lacroix','Adèle',2,0,1),(5,'Roche','Robert',1,0,0),(6,'Poirier','Camille',2,0,0);
/*!40000 ALTER TABLE `candidat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `choix_matiere`
--

DROP TABLE IF EXISTS `choix_matiere`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `choix_matiere` (
  `id_choix_matiere` int NOT NULL AUTO_INCREMENT,
  `id_candidat` int NOT NULL,
  `matiere1` int DEFAULT NULL,
  `matiere2` int DEFAULT NULL,
  PRIMARY KEY (`id_choix_matiere`),
  UNIQUE KEY `UNQ_CANDIDAT` (`id_candidat`),
  KEY `matiere1` (`matiere1`),
  KEY `matiere2` (`matiere2`),
  CONSTRAINT `fk_choix_matiere_id_candidat` FOREIGN KEY (`id_candidat`) REFERENCES `candidat` (`id_candidat`),
  CONSTRAINT `fk_choix_matiere_matiere1` FOREIGN KEY (`matiere1`) REFERENCES `matiere` (`id_matiere`),
  CONSTRAINT `fk_choix_matiere_matiere2` FOREIGN KEY (`matiere2`) REFERENCES `matiere` (`id_matiere`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `choix_matiere`
--

LOCK TABLES `choix_matiere` WRITE;
/*!40000 ALTER TABLE `choix_matiere` DISABLE KEYS */;
INSERT INTO `choix_matiere` VALUES (1,1,13,11),(2,2,15,9),(3,3,16,6),(4,4,14,4),(5,5,2,13),(6,6,14,3);
/*!40000 ALTER TABLE `choix_matiere` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `creneau`
--

DROP TABLE IF EXISTS `creneau`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `creneau` (
  `id_creneau` int NOT NULL AUTO_INCREMENT,
  `id_candidat` int NOT NULL,
  `id_matiere` int NOT NULL,
  `id_salle` int NOT NULL,
  `debut_preparation` datetime NOT NULL,
  `fin_preparation` datetime NOT NULL,
  `fin` datetime NOT NULL,
  PRIMARY KEY (`id_creneau`),
  UNIQUE KEY `UNQ_CANDIDAT_MATIERE` (`id_candidat`,`id_matiere`),
  UNIQUE KEY `UNQ_CANDIDAT_PREPA` (`id_candidat`,`debut_preparation`),
  KEY `id_matiere` (`id_matiere`),
  KEY `id_salle` (`id_salle`),
  CONSTRAINT `fk_creneau_id_candidat` FOREIGN KEY (`id_candidat`) REFERENCES `candidat` (`id_candidat`),
  CONSTRAINT `fk_creneau_id_matiere` FOREIGN KEY (`id_matiere`) REFERENCES `matiere` (`id_matiere`),
  CONSTRAINT `fk_creneau_id_salle` FOREIGN KEY (`id_salle`) REFERENCES `salle` (`id_salle`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `creneau`
--

LOCK TABLES `creneau` WRITE;
/*!40000 ALTER TABLE `creneau` DISABLE KEYS */;
INSERT INTO `creneau` VALUES (1,6,14,6,'2022-03-01 08:00:00','2022-03-01 08:10:00','2022-03-01 08:30:00'),(2,6,3,3,'2022-03-01 09:00:00','2022-03-01 09:30:00','2022-03-01 10:00:00'),(3,2,15,5,'2022-03-01 08:00:00','2022-03-01 08:15:00','2022-03-01 08:45:00'),(4,2,9,3,'2022-03-01 09:30:00','2022-03-01 10:10:00','2022-03-01 10:50:00'),(5,1,13,4,'2022-03-01 08:00:00','2022-03-01 08:10:00','2022-03-01 08:30:00'),(6,1,11,2,'2022-03-01 09:00:00','2022-03-01 09:10:00','2022-03-01 09:30:00'),(7,3,16,2,'2022-03-01 08:00:00','2022-03-01 08:10:00','2022-03-01 08:30:00'),(8,3,6,1,'2022-03-01 09:00:00','2022-03-01 09:30:00','2022-03-01 10:00:00'),(9,5,2,1,'2022-03-01 08:00:00','2022-03-01 08:30:00','2022-03-01 09:00:00'),(10,5,13,4,'2022-03-01 09:30:00','2022-03-01 09:40:00','2022-03-01 10:00:00');
/*!40000 ALTER TABLE `creneau` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `horaire`
--

DROP TABLE IF EXISTS `horaire`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `horaire` (
  `id_horaire` int NOT NULL AUTO_INCREMENT,
  `horaire_arr1` datetime NOT NULL,
  `horaire_dep1` datetime NOT NULL,
  `horaire_arr2` datetime NOT NULL,
  `horaire_dep2` datetime NOT NULL,
  `horaire_arr3` datetime NOT NULL,
  `horaire_dep3` datetime NOT NULL,
  `id_professeur` int NOT NULL,
  PRIMARY KEY (`id_horaire`),
  KEY `fk_horraire_id_professeur` (`id_professeur`),
  CONSTRAINT `fk_horraire_id_professeur` FOREIGN KEY (`id_professeur`) REFERENCES `professeur` (`id_professeur`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `horaire`
--

LOCK TABLES `horaire` WRITE;
/*!40000 ALTER TABLE `horaire` DISABLE KEYS */;
INSERT INTO `horaire` VALUES (1,'1900-01-01 08:00:00','1900-01-01 20:00:00','1900-01-02 08:00:00','1900-01-02 20:00:00','1900-01-03 08:00:00','1900-01-03 20:00:00',1),(2,'1900-01-01 08:00:00','1900-01-01 20:00:00','1900-01-02 08:00:00','1900-01-02 20:00:00','1900-01-03 08:00:00','1900-01-03 20:00:00',2),(3,'1900-01-01 08:00:00','1900-01-01 20:00:00','1900-01-02 08:00:00','1900-01-02 20:00:00','1900-01-03 08:00:00','1900-01-03 20:00:00',3),(4,'1900-01-01 08:00:00','1900-01-01 20:00:00','1900-01-02 08:00:00','1900-01-02 20:00:00','1900-01-03 08:00:00','1900-01-03 20:00:00',4),(5,'1900-01-01 08:00:00','1900-01-01 20:00:00','1900-01-02 08:00:00','1900-01-02 20:00:00','1900-01-03 08:00:00','1900-01-03 20:00:00',5),(6,'1900-01-01 08:00:00','1900-01-01 20:00:00','1900-01-02 08:00:00','1900-01-02 20:00:00','1900-01-03 08:00:00','1900-01-03 20:00:00',6),(7,'1900-01-01 08:00:00','1900-01-01 20:00:00','1900-01-02 08:00:00','1900-01-02 20:00:00','1900-01-03 08:00:00','1900-01-03 20:00:00',7);
/*!40000 ALTER TABLE `horaire` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `liste_matiere`
--

DROP TABLE IF EXISTS `liste_matiere`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `liste_matiere` (
  `id_liste_matiere` int NOT NULL AUTO_INCREMENT,
  `id_professeur` int NOT NULL,
  `id_matiere` int NOT NULL,
  PRIMARY KEY (`id_liste_matiere`),
  UNIQUE KEY `UNQ_PROFESSEUR_MATIERE` (`id_professeur`,`id_matiere`),
  KEY `id_matiere` (`id_matiere`),
  CONSTRAINT `fk_liste_matiere_id_matiere` FOREIGN KEY (`id_matiere`) REFERENCES `matiere` (`id_matiere`),
  CONSTRAINT `fk_liste_matiere_id_professeur` FOREIGN KEY (`id_professeur`) REFERENCES `professeur` (`id_professeur`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `liste_matiere`
--

LOCK TABLES `liste_matiere` WRITE;
/*!40000 ALTER TABLE `liste_matiere` DISABLE KEYS */;
INSERT INTO `liste_matiere` VALUES (27,1,12),(28,1,13),(23,2,2),(24,2,4),(25,2,6),(26,2,10),(8,3,16),(9,4,11),(30,5,14),(19,6,1),(20,6,3),(21,6,5),(22,6,9),(31,7,15);
/*!40000 ALTER TABLE `liste_matiere` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matiere`
--

DROP TABLE IF EXISTS `matiere`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matiere` (
  `id_matiere` int NOT NULL AUTO_INCREMENT,
  `id_serie` int NOT NULL,
  `nom` varchar(30) NOT NULL,
  `nom_complet` varchar(60) NOT NULL,
  `temps_preparation` int NOT NULL,
  `temps_preparation_tiers_temps` int NOT NULL,
  `temps_passage` int NOT NULL,
  `temps_passage_tiers_temps` int NOT NULL,
  `loge` int DEFAULT NULL,
  PRIMARY KEY (`id_matiere`),
  UNIQUE KEY `UNQ_NOM_NOMCOMP_TPS_PREPA` (`nom`,`nom_complet`,`temps_preparation`,`temps_passage`),
  KEY `fk_matiere_salle` (`loge`),
  KEY `id_serie` (`id_serie`),
  CONSTRAINT `fk_matiere_salle` FOREIGN KEY (`loge`) REFERENCES `salle` (`id_salle`),
  CONSTRAINT `fk_matiere_serie` FOREIGN KEY (`id_serie`) REFERENCES `serie` (`id_serie`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matiere`
--

LOCK TABLES `matiere` WRITE;
/*!40000 ALTER TABLE `matiere` DISABLE KEYS */;
INSERT INTO `matiere` VALUES (1,1,'Français','Français - SVT/Mathématiques',30,40,30,40,NULL),(2,1,'Philosophie','Philosophie - SVT/Mathématiques',30,40,30,40,NULL),(3,2,'Français','Français - Mathématique',30,40,30,40,NULL),(4,2,'Philosophie','Philosophie - Mathématique',30,40,30,40,NULL),(5,4,'Français','Français - Anglais avancé/Mathématiques',30,40,30,40,NULL),(6,4,'Philosophie','Philosophie - Anglais avancé/Mathématiques',30,40,30,40,NULL),(9,6,'Français','Français - Mécanique',30,40,30,40,NULL),(10,6,'Philosophie','Philosophie - Mécanique',30,40,30,40,NULL),(11,1,'SVT','SVT - SVT/Mathématiques',10,15,20,30,NULL),(12,4,'Mathématiques','Mathématiques - Anglais avancé/Mathématiques',10,15,20,30,NULL),(13,1,'Mathématiques','Mathématiques - SVT/Mathématiques',10,15,20,30,NULL),(14,2,'Mathématiques','Mathématiques - Mathématique',10,15,20,30,NULL),(15,6,'Mécanique','Mécanique - Mécanique',10,15,20,30,4),(16,4,'Anglais','Anglais - Anglais avancé/Mathématiques',10,15,20,30,2);
/*!40000 ALTER TABLE `matiere` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `professeur`
--

DROP TABLE IF EXISTS `professeur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `professeur` (
  `id_professeur` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(30) NOT NULL,
  `prenom` varchar(30) NOT NULL,
  `salle` int DEFAULT NULL,
  PRIMARY KEY (`id_professeur`),
  KEY `salle` (`salle`),
  CONSTRAINT `fk_professeur__salle_salle` FOREIGN KEY (`salle`) REFERENCES `salle` (`id_salle`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `professeur`
--

LOCK TABLES `professeur` WRITE;
/*!40000 ALTER TABLE `professeur` DISABLE KEYS */;
INSERT INTO `professeur` VALUES (1,'Dupond','Louis',4),(2,'Delacour','Ives',1),(3,'Yon','Paula',2),(4,'Lemallier','Martin',2),(5,'Mireuil','Frederic',6),(6,'Rabotin','Floriane',3),(7,'Dupuis','Gislain',5);
/*!40000 ALTER TABLE `professeur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salle`
--

DROP TABLE IF EXISTS `salle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salle` (
  `id_salle` int NOT NULL AUTO_INCREMENT,
  `numero` varchar(50) NOT NULL,
  PRIMARY KEY (`id_salle`),
  UNIQUE KEY `UNQ_NUMERO` (`numero`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salle`
--

LOCK TABLES `salle` WRITE;
/*!40000 ALTER TABLE `salle` DISABLE KEYS */;
INSERT INTO `salle` VALUES (1,'C002'),(6,'C004'),(4,'D005'),(2,'D202'),(5,'D207'),(3,'D306');
/*!40000 ALTER TABLE `salle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serie`
--

DROP TABLE IF EXISTS `serie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `serie` (
  `id_serie` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(40) NOT NULL,
  `specialite1` varchar(50) DEFAULT NULL,
  `specialite2` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_serie`),
  UNIQUE KEY `UNQ_NOM_SPE1_SPE2` (`nom`,`specialite1`,`specialite2`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serie`
--

LOCK TABLES `serie` WRITE;
/*!40000 ALTER TABLE `serie` DISABLE KEYS */;
INSERT INTO `serie` VALUES (4,'Générale',NULL,NULL),(1,'Générale',NULL, NULL),(2,'Technologique','Mathématique',NULL),(6,'Technologique','Mécanique',NULL);
/*!40000 ALTER TABLE `serie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token`
--

DROP TABLE IF EXISTS `token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token` (
  `id_token` int NOT NULL AUTO_INCREMENT,
  `email` varchar(200) NOT NULL,
  `token` varchar(200) NOT NULL,
  `id_professeur` int DEFAULT NULL,
  `admin` tinyint(1) NOT NULL,
  PRIMARY KEY (`id_token`),
  UNIQUE KEY `unique_token` (`token`),
  KEY `id_professeur` (`id_professeur`),
  CONSTRAINT `fk_token_id_professeur` FOREIGN KEY (`id_professeur`) REFERENCES `professeur` (`id_professeur`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token`
--

LOCK TABLES `token` WRITE;
/*!40000 ALTER TABLE `token` DISABLE KEYS */;
INSERT INTO `token` VALUES (1,'louis.dupond@mail.com','2a1ae4c1-11e0-4e80-bacc-d7abeb81748f',1,0),(2,'ives.delacour@mail.com','e651149f-b262-4cbf-840f-9088bc9b8844',2,0),(3,'paula.yon@mail.com','2980614b-8961-4251-bab7-a7c71e9f2fe4',3,0),(4,'martin.lemallier@mail.com','51d4f62b-179b-41d0-800c-dadcc0bf77fd',4,0),(5,'frederic.mireuil@mail.com','dae75be4-f218-4749-b447-f28554713521',5,0),(6,'floriane.rabotin@mail.com','2125455c-38b2-4bbd-8181-93bf6246543a',6,0),(7,'gislain.dupuis@mail.com','f2825932-d140-4cf2-8250-2b1cb4ec83b7',7,0);
/*!40000 ALTER TABLE `token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utilisateur`
--

DROP TABLE IF EXISTS `utilisateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utilisateur` (
  `id_utilisateur` int NOT NULL AUTO_INCREMENT,
  `email` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  `admin` tinyint(1) NOT NULL,
  `id_professeur` int DEFAULT NULL,
  PRIMARY KEY (`id_utilisateur`),
  UNIQUE KEY `UNQ_utilisateur_email` (`email`,`admin`),
  KEY `id_professeur` (`id_professeur`),
  CONSTRAINT `fk_utilisateur_id_professeur` FOREIGN KEY (`id_professeur`) REFERENCES `professeur` (`id_professeur`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utilisateur`
--

LOCK TABLES `utilisateur` WRITE;
/*!40000 ALTER TABLE `utilisateur` DISABLE KEYS */;
INSERT INTO `utilisateur` VALUES (1,'admin@ac-poitiers.fr','$p5k2$3e8$AfpOzesj$.KoGR.raCRkA3gne.aZrF1bQobRfdSIH',1,NULL);
/*!40000 ALTER TABLE `utilisateur` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-03-08 16:57:49
