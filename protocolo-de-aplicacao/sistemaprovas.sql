-- MySQL dump 10.13  Distrib 8.0.22, for Linux (x86_64)
--
-- Host: localhost    Database: sistemaProvas
-- ------------------------------------------------------
-- Server version	8.0.23-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Alternativa`
--

DROP TABLE IF EXISTS `Alternativa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Alternativa` (
  `codigo` varchar(45) NOT NULL,
  `idQuestao` int NOT NULL,
  `descricao` varchar(45) NOT NULL,
  PRIMARY KEY (`codigo`),
  KEY `fk_Alternativa_Questao1_idx` (`idQuestao`),
  CONSTRAINT `fk_Alternativa_Questao1` FOREIGN KEY (`idQuestao`) REFERENCES `Questao` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Alternativa`
--

LOCK TABLES `Alternativa` WRITE;
/*!40000 ALTER TABLE `Alternativa` DISABLE KEYS */;
INSERT INTO `Alternativa` VALUES ('p2q2a',5,'Linux'),('p2q2b',5,'Windows'),('p2q2c',5,'Mac'),('v1p1',1,'Verde'),('v2p1',1,'Amarelo'),('v3p1',1,'Azul'),('v4p1',2,'2'),('v5p1',2,'4'),('v6p1',2,'5');
/*!40000 ALTER TABLE `Alternativa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Aluno`
--

DROP TABLE IF EXISTS `Aluno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Aluno` (
  `senha` varchar(45) NOT NULL,
  `login` varchar(45) NOT NULL,
  `token` varchar(45) NOT NULL,
  `ativo` int NOT NULL,
  PRIMARY KEY (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Aluno`
--

LOCK TABLES `Aluno` WRITE;
/*!40000 ALTER TABLE `Aluno` DISABLE KEYS */;
INSERT INTO `Aluno` VALUES ('123','Osvaldo','aaa',1),('123','Marcelo','abc',1),('123','Marcelo-Osval','PTC',0),('123','Marcelo-Osvalo','PTC-2021',0),('123','Marcelo-Osvaldo','PTC2021',0);
/*!40000 ALTER TABLE `Aluno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Aluno_Prova`
--

DROP TABLE IF EXISTS `Aluno_Prova`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Aluno_Prova` (
  `tokenAluno` varchar(45) NOT NULL,
  `codigoProva` varchar(45) NOT NULL,
  `nota` int DEFAULT NULL,
  `respostas` varchar(600) DEFAULT NULL,
  PRIMARY KEY (`tokenAluno`,`codigoProva`),
  KEY `fk_Aluno_has_Prova_Prova1_idx` (`codigoProva`),
  KEY `fk_Aluno_has_Prova_Aluno1_idx` (`tokenAluno`),
  CONSTRAINT `fk_Aluno_has_Prova_Aluno1` FOREIGN KEY (`tokenAluno`) REFERENCES `Aluno` (`token`),
  CONSTRAINT `fk_Aluno_has_Prova_Prova1` FOREIGN KEY (`codigoProva`) REFERENCES `Prova` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Aluno_Prova`
--

LOCK TABLES `Aluno_Prova` WRITE;
/*!40000 ALTER TABLE `Aluno_Prova` DISABLE KEYS */;
/*!40000 ALTER TABLE `Aluno_Prova` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Prova`
--

DROP TABLE IF EXISTS `Prova`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Prova` (
  `codigo` varchar(45) NOT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Prova`
--

LOCK TABLES `Prova` WRITE;
/*!40000 ALTER TABLE `Prova` DISABLE KEYS */;
INSERT INTO `Prova` VALUES ('prova1'),('prova2');
/*!40000 ALTER TABLE `Prova` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Questao`
--

DROP TABLE IF EXISTS `Questao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Questao` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ponto` int NOT NULL,
  `enunciado` varchar(200) NOT NULL,
  `codigoProva` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_Questao_Prova_idx` (`codigoProva`),
  CONSTRAINT `fk_Questao_Prova` FOREIGN KEY (`codigoProva`) REFERENCES `Prova` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Questao`
--

LOCK TABLES `Questao` WRITE;
/*!40000 ALTER TABLE `Questao` DISABLE KEYS */;
INSERT INTO `Questao` VALUES (1,5,'Qual a cor dor mar?','prova1'),(2,5,'Quais dos números são pares?','prova1'),(3,1,'Descreva o teorema da informação','prova1'),(4,2,'Qual o seu sistema opracional?','prova2'),(5,4,'Qual sistema possui código aberto?','prova2'),(6,4,'O que é um sistema operacional?','prova2');
/*!40000 ALTER TABLE `Questao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Resposta`
--

DROP TABLE IF EXISTS `Resposta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Resposta` (
  `id` int NOT NULL,
  `idQuestao` int NOT NULL,
  `codigoAlternativa` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_Resposta_Questao1_idx` (`idQuestao`),
  KEY `fk_Resposta_Alternativa1_idx` (`codigoAlternativa`),
  CONSTRAINT `fk_Resposta_Alternativa1` FOREIGN KEY (`codigoAlternativa`) REFERENCES `Alternativa` (`codigo`),
  CONSTRAINT `fk_Resposta_Questao1` FOREIGN KEY (`idQuestao`) REFERENCES `Questao` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Resposta`
--

LOCK TABLES `Resposta` WRITE;
/*!40000 ALTER TABLE `Resposta` DISABLE KEYS */;
INSERT INTO `Resposta` VALUES (1,1,'v3p1'),(2,2,'v4p1'),(3,2,'v5p1'),(4,5,'p2q2a');
/*!40000 ALTER TABLE `Resposta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-05 13:05:58
