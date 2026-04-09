-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: django
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `api_aichatmessage`
--

DROP TABLE IF EXISTS `api_aichatmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_aichatmessage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sender` varchar(50) NOT NULL,
  `message` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `confidence_score` int DEFAULT NULL,
  `likely_causes` json NOT NULL,
  `recommended_actions` json NOT NULL,
  `patient_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_aichatmessage_patient_id_6108004d_fk_api_patient_id` (`patient_id`),
  CONSTRAINT `api_aichatmessage_patient_id_6108004d_fk_api_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `api_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_aichatmessage`
--

LOCK TABLES `api_aichatmessage` WRITE;
/*!40000 ALTER TABLE `api_aichatmessage` DISABLE KEYS */;
INSERT INTO `api_aichatmessage` VALUES (1,'user','hlo','2026-03-17 07:14:33.366190',NULL,'[]','[]',NULL),(2,'ai','Based on the patient\'s current waveform data and history, here is my analysis.','2026-03-17 07:14:33.473630',85,'[{\"cause\": \"Secretions/Mucus Plug\", \"probability\": \"85%\"}, {\"cause\": \"Patient Agitation\", \"probability\": \"60%\"}, {\"cause\": \"Tube Kinking\", \"probability\": \"45%\"}]','[\"Suction the airway to clear secretions\", \"Check sedation levels (RASS score)\", \"Verify tube positioning\"]',NULL),(3,'user','okey','2026-03-17 07:14:49.541837',NULL,'[]','[]',NULL),(4,'ai','Based on the patient\'s current waveform data and history, here is my analysis.','2026-03-17 07:14:49.545849',85,'[{\"cause\": \"Secretions/Mucus Plug\", \"probability\": \"85%\"}, {\"cause\": \"Patient Agitation\", \"probability\": \"60%\"}, {\"cause\": \"Tube Kinking\", \"probability\": \"45%\"}]','[\"Suction the airway to clear secretions\", \"Check sedation levels (RASS score)\", \"Verify tube positioning\"]',NULL),(5,'user','what we do','2026-03-17 07:15:21.010234',NULL,'[]','[]',NULL),(6,'ai','Based on the patient\'s current waveform data and history, here is my analysis.','2026-03-17 07:15:21.026111',85,'[{\"cause\": \"Secretions/Mucus Plug\", \"probability\": \"85%\"}, {\"cause\": \"Patient Agitation\", \"probability\": \"60%\"}, {\"cause\": \"Tube Kinking\", \"probability\": \"45%\"}]','[\"Suction the airway to clear secretions\", \"Check sedation levels (RASS score)\", \"Verify tube positioning\"]',NULL),(7,'user','hlo','2026-03-17 07:26:05.172020',NULL,'[]','[]',NULL),(8,'ai','Based on the input and current ventilator parameters, the patient appears relatively stable, but continuous monitoring is advised. Could you provide more specific symptoms or parameters (like pressure, volume, or SpO2)?','2026-03-17 07:26:05.204510',75,'[]','[]',NULL),(9,'user','vijay aney person ki spo2 ekkuva ayyindhi eppudu nenu em cheyyali','2026-03-17 07:26:43.537402',NULL,'[]','[]',NULL),(10,'ai','Desaturation noted. Before increasing FiO2, consider checking airway patency.','2026-03-17 07:26:43.542449',94,'[{\"cause\": \"Mucus Plugging\", \"probability\": \"75%\"}, {\"cause\": \"Loss of PEEP\", \"probability\": \"60%\"}, {\"cause\": \"Ventilator Asynchrony\", \"probability\": \"55%\"}]','[\"Briefly increase FiO2 to 100% (100% O2 suction mode)\", \"Suction patient if secretions suspected\", \"Assess for signs of pneumothorax if sudden\"]',NULL),(11,'user','okey','2026-03-17 07:26:54.313890',NULL,'[]','[]',NULL),(12,'ai','Based on the input and current ventilator parameters, the patient appears relatively stable, but continuous monitoring is advised. Could you provide more specific symptoms or parameters (like pressure, volume, or SpO2)?','2026-03-17 07:26:54.319839',75,'[]','[]',NULL),(13,'user','oye','2026-03-17 07:27:00.500733',NULL,'[]','[]',NULL),(14,'ai','Based on the input and current ventilator parameters, the patient appears relatively stable, but continuous monitoring is advised. Could you provide more specific symptoms or parameters (like pressure, volume, or SpO2)?','2026-03-17 07:27:00.503428',75,'[]','[]',NULL),(15,'user','hlo','2026-03-17 07:27:06.071818',NULL,'[]','[]',NULL),(16,'ai','Based on the input and current ventilator parameters, the patient appears relatively stable, but continuous monitoring is advised. Could you provide more specific symptoms or parameters (like pressure, volume, or SpO2)?','2026-03-17 07:27:06.075817',75,'[]','[]',NULL),(17,'user','hd7rbir','2026-03-17 07:27:24.168254',NULL,'[]','[]',NULL),(18,'ai','Based on the input and current ventilator parameters, the patient appears relatively stable, but continuous monitoring is advised. Could you provide more specific symptoms or parameters (like pressure, volume, or SpO2)?','2026-03-17 07:27:24.170760',75,'[]','[]',NULL);
/*!40000 ALTER TABLE `api_aichatmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_aipredictedevent`
--

DROP TABLE IF EXISTS `api_aipredictedevent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_aipredictedevent` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `event_name` varchar(200) NOT NULL,
  `time_to_event` varchar(50) NOT NULL,
  `confidence_score` int NOT NULL,
  `recommendation` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `patient_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_aipredictedevent_patient_id_89e46be8_fk_api_patient_id` (`patient_id`),
  CONSTRAINT `api_aipredictedevent_patient_id_89e46be8_fk_api_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `api_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_aipredictedevent`
--

LOCK TABLES `api_aipredictedevent` WRITE;
/*!40000 ALTER TABLE `api_aipredictedevent` DISABLE KEYS */;
INSERT INTO `api_aipredictedevent` VALUES (10,'High Peak Pressure','in 2 hours',85,'Monitor vitals','2026-04-01 06:34:07.907987',44),(11,'High Peak Pressure','in 2 hours',85,'Monitor vitals','2026-04-01 06:34:07.916020',45),(12,'High Peak Pressure','in 2 hours',85,'Monitor vitals','2026-04-01 06:34:07.918588',46),(13,'High Peak Pressure','in 2 hours',85,'Monitor vitals','2026-04-01 06:34:07.920366',50);
/*!40000 ALTER TABLE `api_aipredictedevent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_alert`
--

DROP TABLE IF EXISTS `api_alert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_alert` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `alert_type` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `status` varchar(50) NOT NULL,
  `escalated_to_id` int DEFAULT NULL,
  `device_id` bigint DEFAULT NULL,
  `patient_id` bigint NOT NULL,
  `ai_confidence` int DEFAULT NULL,
  `current_value` varchar(50) DEFAULT NULL,
  `limit_value` varchar(50) DEFAULT NULL,
  `probable_cause` longtext,
  `suggested_action` longtext,
  PRIMARY KEY (`id`),
  KEY `api_alert_escalated_to_id_2f734f69_fk_auth_user_id` (`escalated_to_id`),
  KEY `api_alert_device_id_04f4dd80_fk_api_device_id` (`device_id`),
  KEY `api_alert_patient_id_3afa6e04_fk_api_patient_id` (`patient_id`),
  CONSTRAINT `api_alert_device_id_04f4dd80_fk_api_device_id` FOREIGN KEY (`device_id`) REFERENCES `api_device` (`id`),
  CONSTRAINT `api_alert_escalated_to_id_2f734f69_fk_auth_user_id` FOREIGN KEY (`escalated_to_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `api_alert_patient_id_3afa6e04_fk_api_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `api_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_alert`
--

LOCK TABLES `api_alert` WRITE;
/*!40000 ALTER TABLE `api_alert` DISABLE KEYS */;
INSERT INTO `api_alert` VALUES (9,'Critical','High Heart Rate (Tachycardia)','2026-03-11 09:24:50.120778','Active',NULL,NULL,44,85,'115 bpm','100 bpm',NULL,NULL),(10,'Warning','Low SpO2 level detected','2026-03-11 09:24:50.126593','Active',NULL,NULL,45,92,'91%','94%',NULL,NULL),(11,'Critical','Sudden drop in Blood Pressure','2026-03-11 09:24:50.131571','Active',NULL,NULL,46,88,'90/60','110/70',NULL,NULL),(12,'Warning','Irregular Respiratory Rate','2026-03-11 09:24:50.135793','Active',NULL,NULL,47,75,'28 bpm','20 bpm',NULL,NULL);
/*!40000 ALTER TABLE `api_alert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_alertsetting`
--

DROP TABLE IF EXISTS `api_alertsetting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_alertsetting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `push_notifications` tinyint(1) NOT NULL,
  `sound` tinyint(1) NOT NULL,
  `vibration` tinyint(1) NOT NULL,
  `spo2_low_limit` int NOT NULL,
  `rr_high_limit` int NOT NULL,
  `pressure_high_limit` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `api_alertsetting_user_id_15fa7c4d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_alertsetting`
--

LOCK TABLES `api_alertsetting` WRITE;
/*!40000 ALTER TABLE `api_alertsetting` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_alertsetting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_anomaly`
--

DROP TABLE IF EXISTS `api_anomaly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_anomaly` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `anomaly_type` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `confidence_score` int NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `is_reviewed` tinyint(1) NOT NULL,
  `patient_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_anomaly_patient_id_fa7a61ee_fk_api_patient_id` (`patient_id`),
  CONSTRAINT `api_anomaly_patient_id_fa7a61ee_fk_api_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `api_patient` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_anomaly`
--

LOCK TABLES `api_anomaly` WRITE;
/*!40000 ALTER TABLE `api_anomaly` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_anomaly` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_appearancesetting`
--

DROP TABLE IF EXISTS `api_appearancesetting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_appearancesetting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `theme_preference` varchar(20) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `api_appearancesetting_user_id_f06e33d7_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_appearancesetting`
--

LOCK TABLES `api_appearancesetting` WRITE;
/*!40000 ALTER TABLE `api_appearancesetting` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_appearancesetting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_auditlog`
--

DROP TABLE IF EXISTS `api_auditlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_auditlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `system_actor` varchar(100) DEFAULT NULL,
  `action` varchar(255) NOT NULL,
  `details` varchar(255) DEFAULT NULL,
  `icon_type` varchar(50) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_auditlog_user_id_b15d4175_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_auditlog_user_id_b15d4175_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_auditlog`
--

LOCK TABLES `api_auditlog` WRITE;
/*!40000 ALTER TABLE `api_auditlog` DISABLE KEYS */;
INSERT INTO `api_auditlog` VALUES (1,NULL,'Approved User','chanikyathottempudi9999@gmail.com','user','2026-03-26 05:18:01.852231',13),(2,NULL,'Approved User','abhi12@gmail.com','user','2026-03-28 04:20:20.077004',13),(3,NULL,'Approved User','abhi12@gmail.com','user','2026-03-28 04:21:10.080540',13),(4,NULL,'Approved User','abhi12@gmail.com','user','2026-03-28 04:21:29.533847',13),(5,NULL,'Approved User','kush234@gmail.com','user','2026-03-31 09:07:29.547714',13),(6,NULL,'Approved User','admin@gmail.com','user','2026-03-31 09:07:50.022230',13),(7,NULL,'Deleted Patient Record','Patient jithendra','warning','2026-04-01 05:07:08.744605',43),(8,NULL,'Promoted to Admin','kush234@gmail.com','admin','2026-04-01 05:23:35.189337',13),(9,NULL,'Dismissed Admin','kush234@gmail.com','warning','2026-04-01 05:24:46.696654',13),(10,NULL,'Approved User','ram12@gmail.com','user','2026-04-01 08:01:05.352780',13),(11,NULL,'Approved User','kakumanisainithin@gmail.com','user','2026-04-06 08:59:04.200680',13);
/*!40000 ALTER TABLE `api_auditlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_device`
--

DROP TABLE IF EXISTS `api_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_device` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mac_address` varchar(50) NOT NULL,
  `device_type` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  `current_settings` json NOT NULL,
  `assigned_patient_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mac_address` (`mac_address`),
  UNIQUE KEY `assigned_patient_id` (`assigned_patient_id`),
  CONSTRAINT `api_device_assigned_patient_id_bfb358b9_fk_api_patient_id` FOREIGN KEY (`assigned_patient_id`) REFERENCES `api_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_device`
--

LOCK TABLES `api_device` WRITE;
/*!40000 ALTER TABLE `api_device` DISABLE KEYS */;
INSERT INTO `api_device` VALUES (41,'MAC:P101','Ventilator','Active','{\"rr\": \"24\", \"tv\": \"416\", \"fio2\": \"70%\", \"mode\": \"AC/VC Mode\", \"peep\": \"10.0\"}',44),(42,'MAC:P102','Ventilator','Active','{\"rr\": \"16\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',45),(43,'MAC:P103','Ventilator','Active','{\"rr\": \"15\", \"tv\": \"450\", \"fio2\": \"40%\", \"mode\": \"AC/VC Mode\", \"peep\": \"8.0\"}',46),(44,'MAC:P104','Ventilator','Active','{\"rr\": \"14\", \"tv\": \"450\", \"fio2\": \"35%\", \"mode\": \"AC/VC Mode\", \"peep\": \"7.5\"}',47),(45,'MAC:P105','Ventilator','Active','{\"rr\": \"21\", \"tv\": \"450\", \"fio2\": \"40%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',48),(46,'MAC:P106','Ventilator','Active','{\"rr\": \"14\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',49),(47,'MAC:P107','Ventilator','Active','{\"rr\": \"22\", \"tv\": \"450\", \"fio2\": \"30%\", \"mode\": \"SIMV Mode\", \"peep\": \"6.0\"}',50),(48,'MAC:P108','Ventilator','Active','{\"rr\": \"14\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',51),(49,'MAC:P109','Ventilator','Active','{\"rr\": \"14\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',52),(50,'MAC:P110','Ventilator','Active','{\"rr\": \"17\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',53),(51,'MAC:P111','Ventilator','Active','{\"rr\": \"15\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',54),(52,'MAC:P112','Ventilator','Active','{\"rr\": \"14\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',55),(53,'MAC:P113','Ventilator','Active','{\"rr\": \"14\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',56),(54,'MAC:P114','Ventilator','Active','{\"rr\": \"17\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',57),(55,'MAC:P115','Ventilator','Active','{\"rr\": \"16\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',58),(56,'MAC:P116','Ventilator','Active','{\"rr\": \"18\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',59),(57,'MAC:P117','Ventilator','Active','{\"rr\": \"15\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',60),(58,'MAC:P118','Ventilator','Active','{\"rr\": \"18\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',61),(59,'MAC:P119','Ventilator','Active','{\"rr\": \"16\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',62),(60,'MAC:P120','Ventilator','Active','{\"rr\": \"14\", \"tv\": \"450\", \"fio2\": \"21%\", \"mode\": \"AC/VC Mode\", \"peep\": \"5.0\"}',63);
/*!40000 ALTER TABLE `api_device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_faq`
--

DROP TABLE IF EXISTS `api_faq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_faq` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `selected_topic` varchar(200) NOT NULL,
  `answer` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `order` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_faq`
--

LOCK TABLES `api_faq` WRITE;
/*!40000 ALTER TABLE `api_faq` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_faq` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_loginhistory`
--

DROP TABLE IF EXISTS `api_loginhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_loginhistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `device_name` varchar(100) NOT NULL,
  `location` varchar(100) DEFAULT NULL,
  `login_time` datetime(6) NOT NULL,
  `is_password_change` tinyint(1) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_loginhistory_user_id_895493a5_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_loginhistory_user_id_895493a5_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_loginhistory`
--

LOCK TABLES `api_loginhistory` WRITE;
/*!40000 ALTER TABLE `api_loginhistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_loginhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_notification`
--

DROP TABLE IF EXISTS `api_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `target_user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_notification_user_id_6cede59e_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_notification_user_id_6cede59e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_notification`
--

LOCK TABLES `api_notification` WRITE;
/*!40000 ALTER TABLE `api_notification` DISABLE KEYS */;
INSERT INTO `api_notification` VALUES (2,'New User Signup','Dr.Anantha Reddy has requested access as a doctor.',0,'2026-03-18 20:04:12.974292',12,14),(3,'New User Signup','Dr.Anantha Reddy has requested access as a doctor.',0,'2026-03-18 20:04:12.976310',13,14),(7,'New User Signup','Dr Ajay Reddy has requested access as a doctor.',0,'2026-03-18 20:33:29.765664',12,15),(8,'New User Signup','Dr Ajay Reddy has requested access as a doctor.',0,'2026-03-18 20:33:29.767832',13,15),(13,'New User Signup','dr sai has requested access as a Nurse.',0,'2026-03-19 03:43:39.373293',12,16),(14,'New User Signup','dr sai has requested access as a Nurse.',0,'2026-03-19 03:43:39.375298',13,16),(17,'New User Signup','Fresh Test has requested access as a Doctor.',0,'2026-03-19 05:55:15.527627',12,29),(18,'New User Signup','Fresh Test has requested access as a Doctor.',0,'2026-03-19 05:55:15.528664',13,29),(20,'New User Signup','dr.sonu has requested access as a Doctor.',0,'2026-03-19 05:58:55.005302',12,30),(21,'New User Signup','dr.sonu has requested access as a Doctor.',0,'2026-03-19 05:58:55.006833',13,30),(23,'New User Signup','Dr.naga has requested access as a Nurse.',0,'2026-03-19 06:01:12.299006',12,31),(24,'New User Signup','Dr.naga has requested access as a Nurse.',0,'2026-03-19 06:01:12.300007',13,31),(27,'New User Signup','dr.bhargav has requested access as a Doctor.',0,'2026-03-19 06:33:03.976926',12,32),(28,'New User Signup','dr.bhargav has requested access as a Doctor.',0,'2026-03-19 06:33:03.977978',13,32),(31,'New User Signup','1 has requested access as a Doctor / Physician.',0,'2026-03-24 08:59:22.851104',12,33),(32,'New User Signup','1 has requested access as a Doctor / Physician.',0,'2026-03-24 08:59:22.853482',13,33),(34,'New User Signup','muffin has requested access as a Doctor / Physician.',0,'2026-03-24 09:14:00.728562',12,34),(35,'New User Signup','muffin has requested access as a Doctor / Physician.',0,'2026-03-24 09:14:00.733560',13,34),(38,'New User Signup','Dr Brahma Reddy has requested access as a Doctor / Physician.',0,'2026-03-25 03:40:01.963623',12,36),(39,'Account Approved','Your account has been approved by the administrator. You can now access the dashboard.',0,'2026-03-25 03:40:37.051857',36,NULL),(40,'Account Approved','Your account has been approved by the administrator. You can now access the dashboard.',0,'2026-03-25 03:40:42.541797',36,NULL),(41,'New User Signup','Dr Naga has requested access as a Doctor / Physician.',0,'2026-03-25 03:48:21.591857',12,37),(42,'Account Approved','Your account has been approved by the administrator. You can now access the dashboard.',0,'2026-03-25 03:48:31.898561',37,NULL),(43,'Account Approved','Your account has been approved by the administrator. You can now access the dashboard.',0,'2026-03-25 03:48:35.830065',37,NULL),(44,'New User Signup','Dr karthik has requested access as a Doctor / Physician.',0,'2026-03-25 04:15:17.886987',12,38),(45,'Account Approved','Your account has been approved by the administrator. You can now access the dashboard.',0,'2026-03-25 04:15:32.618298',38,NULL),(46,'New User Signup','Dr chanikya has requested access as a Doctor / Physician.',0,'2026-03-26 05:17:18.551794',12,39),(48,'New User Signup','Dr abhi has requested access as a Doctor.',0,'2026-03-28 04:19:44.063163',12,40),(49,'Account Approved','Your account has been approved by the administrator. You can now access the dashboard.',0,'2026-03-28 04:20:20.069744',40,NULL),(50,'Account Approved','Your account has been approved by the administrator. You can now access the dashboard.',0,'2026-03-28 04:21:10.074539',40,NULL),(51,'Account Approved','Your account has been approved by the administrator. You can now access the dashboard.',0,'2026-03-28 04:21:29.526056',40,NULL),(52,'New User Signup','Test signup request',1,'2026-03-28 04:33:01.544981',12,41),(53,'New User Signup','Admin has requested access as a Doctor.',1,'2026-03-28 04:44:33.979400',12,42),(54,'New Patient Added','Dr added patient: jithendra',0,'2026-03-28 04:52:15.419825',12,NULL),(55,'New User Signup','Dr kush has requested access as a Doctor.',1,'2026-03-31 09:07:10.705990',12,43),(56,'Account Approved','Your account has been approved by the administrator. You can now access the dashboard.',0,'2026-03-31 09:07:29.532931',43,NULL),(57,'Account Approved','Your account has been approved by the administrator. You can now access the dashboard.',0,'2026-03-31 09:07:50.012684',42,NULL),(58,'New Patient Added','Dr added patient: venkata reddy',0,'2026-04-01 03:20:33.844978',12,NULL),(59,'Patient Record Deleted','Dr kush permanently deleted the record for patient jithendra.',0,'2026-04-01 05:07:08.730806',12,NULL),(60,'Patient Record Deleted','Dr kush permanently deleted the record for patient jithendra.',0,'2026-04-01 05:07:08.740223',13,NULL),(61,'New User Signup','Dr ramanji has requested access as a Doctor / Physician.',1,'2026-04-01 08:00:38.746437',12,44),(62,'Account Approved','Your account has been approved by the administrator. You can now access the dashboard.',0,'2026-04-01 08:01:05.338952',44,NULL),(63,'New Patient Added','Dr added patient: venkat reddy',0,'2026-04-01 08:03:57.558626',12,NULL),(64,'New Patient Added','brahmarreddy added patient: Sai Nithin K',0,'2026-04-06 08:53:56.298459',12,NULL),(65,'New User Signup','dr nithin sai has requested access as a Doctor.',1,'2026-04-06 08:58:42.650019',12,45),(66,'Account Approved','Your account has been approved by the administrator. You can now access the dashboard.',0,'2026-04-06 08:59:04.191033',45,NULL);
/*!40000 ALTER TABLE `api_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_onboardingstep`
--

DROP TABLE IF EXISTS `api_onboardingstep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_onboardingstep` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `image_key` varchar(100) NOT NULL,
  `order` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_onboardingstep`
--

LOCK TABLES `api_onboardingstep` WRITE;
/*!40000 ALTER TABLE `api_onboardingstep` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_onboardingstep` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_otp`
--

DROP TABLE IF EXISTS `api_otp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_otp` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `code` varchar(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_otp`
--

LOCK TABLES `api_otp` WRITE;
/*!40000 ALTER TABLE `api_otp` DISABLE KEYS */;
INSERT INTO `api_otp` VALUES (1,'yathakuntabrahmareddy1115@gmail.com','106670','2026-03-16 05:11:04.481271',0),(2,'yathakuntabrahmareddy1115@gmail.com','587490','2026-03-16 05:11:06.602872',0),(3,'yathakuntabrahmareddy1115@gmail.com','262116','2026-03-16 05:21:29.910614',0),(4,'yathakuntabrahmareddy1115@gmail.com','413407','2026-03-16 05:21:30.666072',0),(5,'yathakuntabrahmareddy1115@gmail.com','622725','2026-03-16 05:21:30.962069',0),(6,'yathakuntabrahmareddy1115@gmail.com','293264','2026-03-16 05:21:31.175351',0),(7,'yathakuntabrahmareddy1115@gmail.com','627742','2026-03-16 05:21:31.344108',0),(8,'yathakuntabrahmareddy1115@gmail.com','548009','2026-03-16 07:31:40.897408',0),(9,'yathakuntabrahmareddy1115@gmail.com','167218','2026-03-16 07:31:40.894384',0),(10,'yathakuntabrahmareddy1115@gmail.com','884932','2026-03-16 07:31:41.142008',0),(11,'yathakuntabrahmareddy1115@gmail.com','245356','2026-03-16 07:31:41.187534',0),(12,'yathakuntabrahmareddy1115@gmail.com','576974','2026-03-16 07:31:41.226839',0),(13,'yathakuntabrahmareddy1115@gmail.com','236035','2026-03-16 07:31:41.228843',0),(14,'yathakuntabrahmareddy1115@gmail.com','552958','2026-03-16 07:31:41.405146',0),(15,'yathakuntabrahmareddy1115@gmail.com','433961','2026-03-16 07:31:41.406647',0),(16,'yathakuntabrahmareddy1115@gmail.com','560828','2026-03-16 07:31:41.581218',0),(17,'yathakuntabrahmareddy1115@gmail.com','519869','2026-03-16 07:31:41.761006',0),(18,'yathakuntabrahmareddy1115@gmail.com','499771','2026-03-16 07:31:41.762531',0),(19,'yathakuntabrahmareddy1115@gmail.com','105445','2026-03-16 07:31:41.853365',0),(20,'yathakuntabrahmareddy1115@gmail.com','264167','2026-03-16 07:31:41.934335',0),(21,'yathakuntabrahmareddy1115@gmail.com','734738','2026-03-16 07:31:41.964948',0),(22,'yathakuntabrahmareddy1115@gmail.com','920095','2026-03-16 07:31:42.098483',0),(23,'yathakuntabrahmareddy1115@gmail.com','170795','2026-03-19 05:22:59.847941',0),(24,'yathakuntabrahmareddy1115@gmail.com','851613','2026-03-19 05:23:26.077423',0),(25,'yeruvanagalakshmi11@gmail.com','960889','2026-03-19 06:02:43.881087',0),(26,'yeruvanagalakshmi11@gmail.com','290229','2026-03-19 06:03:03.253933',0),(27,'yeruvanagalakshmi11@gmnail.com','574210','2026-03-19 06:07:23.899538',0),(28,'yeruvanagalakshmi11@gmail.com','232070','2026-03-19 06:16:45.022536',0),(29,'yeruvanagalakshmi11@gmail.com','414680','2026-03-19 06:19:12.190256',0),(30,'yathakuntabrahmareddy1115@gmail.com','520435','2026-03-19 06:27:30.821722',0),(31,'yathakuntabrahmareddy1115@gmail.com','487946','2026-03-19 06:28:57.721247',1),(32,'yeruvanagalakshmi11@gmail.com','754763','2026-03-19 06:29:54.918074',1),(33,'bhargavsaib1999@gmail.com','484926','2026-03-19 06:34:25.661436',1),(34,'yeruvanagalakshmi11@gmail.com','489019','2026-03-25 03:49:50.978296',1),(35,'yeruvanagalakshmi11@gmail.com','401431','2026-03-25 03:49:55.799643',0),(36,'yeruvanagalakshmi11@gmail.com','315284','2026-03-25 04:32:24.979256',0),(37,'yeruvanagalakshmi11@gmail.com','248382','2026-03-25 05:03:17.288995',1),(38,'yeruvanagalakshmi11@gmail.com','428451','2026-03-26 09:31:06.044215',1),(39,'yeruvanagalakshmi11@gmail.com','153990','2026-03-26 09:36:25.366775',0),(40,'yeruvanagalakshmi11@gmail.com','504888','2026-03-26 09:37:12.601841',0),(41,'yeruvanagalakshmi11@gmail.com','999487','2026-04-01 07:29:33.330792',0),(42,'yeruvanagalakshmi11@gmail.com','841201','2026-04-01 07:31:58.335827',0),(43,'yeruvanagalakshmi11@gmail.com','747079','2026-04-01 07:43:56.581030',1),(44,'yeruvanagalakshmi11@gmail.com','673746','2026-04-01 07:45:27.754738',0),(45,'kakumanisainithin@gmail.com','833082','2026-04-06 09:00:42.227013',0),(46,'kakumanisainithin@gmail.com','193478','2026-04-06 09:02:13.207975',0),(47,'yeruvanagalakshmi11@gmail.com','714052','2026-04-06 09:03:25.800240',0),(48,'kakumanisainithin@gmail.com','908020','2026-04-06 09:11:36.415154',0),(49,'yeruvanagalakshmi11@gmail.com','561412','2026-04-06 09:12:07.643510',0),(50,'yeruvanagalakshmi11@gmail.com','279956','2026-04-06 09:17:47.819718',0),(51,'yeruvanagalakshmi11@gmail.com','856641','2026-04-06 09:23:23.768682',0);
/*!40000 ALTER TABLE `api_otp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_patient`
--

DROP TABLE IF EXISTS `api_patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_patient` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(200) NOT NULL,
  `patient_id` varchar(50) NOT NULL,
  `dob` varchar(50) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `weight` double DEFAULT NULL,
  `primary_diagnosis` varchar(255) DEFAULT NULL,
  `admission_date` varchar(50) DEFAULT NULL,
  `bed_number` varchar(50) DEFAULT NULL,
  `attending_physician` varchar(200) DEFAULT NULL,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `patient_id` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_patient`
--

LOCK TABLES `api_patient` WRITE;
/*!40000 ALTER TABLE `api_patient` DISABLE KEYS */;
INSERT INTO `api_patient` VALUES (44,'Rajesh Kumar','P101','1975-05-12','Male',NULL,'Severe ARDS','2026-03-11','ICU-01','Dr. Sharma','Critical'),(45,'Sneha Sharma','P102','1988-08-22','Female',NULL,'Post-Op Recovery','2026-03-11','ICU-02','Dr. Verma','Warning'),(46,'Amit Patel','P103','1962-11-30','Male',NULL,'Sepsis','2026-03-11','ICU-03','Dr. Iyer','Critical'),(47,'Priya Singh','P104','1995-02-15','Female',NULL,'Heart Failure','2026-03-11','NICU-01','Dr. Reddy','Warning'),(48,'Vikram Singh','P105','1980-03-10','Male',NULL,'Pneumonia','2026-03-11','ICU-04','Dr. Sharma','Stable'),(49,'Anjali Gupta','P106','1992-07-05','Female',NULL,'Asthma Attack','2026-03-11','PICU-01','Dr. Gupta','Stable'),(50,'Suresh Raina','P107','1978-12-18','Male',NULL,'COPD Exacerbation','2026-03-11','ICU-05','Dr. Verma','Critical'),(51,'Meera Iyer','P108','1985-06-25','Female',NULL,'Diabetic Ketoacidosis','2026-03-11','ICU-06','Dr. Iyer','Stable'),(52,'Rahul Dravid','P109','1970-01-11','Male',NULL,'Myocardial Infarction','2026-03-11','CCU-01','Dr. Reddy','Warning'),(53,'Kavita Reddy','P110','1990-09-09','Female',NULL,'Acute Renal Failure','2026-03-11','ICU-07','Dr. Sharma','Stable'),(54,'Manish Malhotra','P111','1965-04-03','Male',NULL,'Stroke','2026-03-11','ER-01','Dr. Gupta','Critical'),(55,'Pooja Hegde','P112','1983-10-13','Female',NULL,'Gastric Perforation','2026-03-11','ICU-08','Dr. Verma','Stable'),(56,'Arjun Kapoor','P113','1987-06-26','Male',NULL,'Fracture Recovery','2026-03-11','Ward-12','Dr. Sharma','Stable'),(57,'Deepa Malik','P114','1972-09-30','Female',NULL,'Spinal Injury','2026-03-11','Ward-15','Dr. Iyer','Stable'),(58,'Rohit Sharma','P115','1987-04-30','Male',NULL,'Post-Op','2026-03-11','ICU-09','Dr. Reddy','Warning'),(59,'Vidya Balan','P116','1979-01-01','Female',NULL,'Fever','2026-03-11','Ward-05','Dr. Sharma','Stable'),(60,'Karan Johar','P117','1972-05-25','Male',NULL,'Chest Pain','2026-03-11','ER-05','Dr. Verma','Warning'),(61,'Shanti Devi','P118','1955-12-12','Female',NULL,'Hypertension','2026-03-11','Ward-10','Dr. Gupta','Stable'),(62,'Gopal Das','P119','1968-02-28','Male',NULL,'Liver Cirrhosis','2026-03-11','Ward-08','Dr. Sharma','Stable'),(63,'Lakshmi Narayan','P120','1982-11-15','Female',NULL,'Anemia','2026-03-11','Ward-02','Dr. Iyer','Stable'),(66,'venkat reddy','p-321','1/4/2004','Male',NULL,'low pressure','31/3/2026','icu-22','Dr. James Chen','Warning'),(67,'Sai Nithin K','p-385','2003-10-24','Male',NULL,'high pressure','2026-04-05','icu69','Dr. Sarah Wilson','Warning');
/*!40000 ALTER TABLE `api_patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_patienthistory`
--

DROP TABLE IF EXISTS `api_patienthistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_patienthistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `timestamp` datetime(6) NOT NULL,
  `patient_id` bigint NOT NULL,
  `recorded_by_id` int DEFAULT NULL,
  `event_description` longtext,
  `event_title` varchar(255) NOT NULL,
  `event_type` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_patienthistory_patient_id_39e22b29_fk_api_patient_id` (`patient_id`),
  KEY `api_patienthistory_recorded_by_id_0ca7ff7e_fk_auth_user_id` (`recorded_by_id`),
  CONSTRAINT `api_patienthistory_patient_id_39e22b29_fk_api_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `api_patient` (`id`),
  CONSTRAINT `api_patienthistory_recorded_by_id_0ca7ff7e_fk_auth_user_id` FOREIGN KEY (`recorded_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_patienthistory`
--

LOCK TABLES `api_patienthistory` WRITE;
/*!40000 ALTER TABLE `api_patienthistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_patienthistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_patientrisk`
--

DROP TABLE IF EXISTS `api_patientrisk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_patientrisk` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `risk_score` int NOT NULL,
  `risk_factors` json NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `patient_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_patientrisk_patient_id_62dec43b_fk_api_patient_id` (`patient_id`),
  CONSTRAINT `api_patientrisk_patient_id_62dec43b_fk_api_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `api_patient` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_patientrisk`
--

LOCK TABLES `api_patientrisk` WRITE;
/*!40000 ALTER TABLE `api_patientrisk` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_patientrisk` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_profile`
--

DROP TABLE IF EXISTS `api_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role` varchar(50) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `hospital` varchar(200) DEFAULT NULL,
  `user_id` int NOT NULL,
  `employee_id` varchar(50) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `is_approved` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `api_profile_user_id_41309820_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_profile`
--

LOCK TABLES `api_profile` WRITE;
/*!40000 ALTER TABLE `api_profile` DISABLE KEYS */;
INSERT INTO `api_profile` VALUES (11,'adminastrator',NULL,NULL,12,NULL,NULL,1),(12,'adminastrator','Intensive Care Unit',NULL,13,NULL,'9573057639',1),(23,'doctor',NULL,NULL,36,NULL,'',1),(24,'doctor',NULL,NULL,37,NULL,'',1),(25,'doctor',NULL,NULL,38,NULL,'9573057639',1),(27,'doctor',NULL,NULL,40,NULL,'8297661566',1),(28,'nurse',NULL,NULL,41,NULL,NULL,1),(29,'doctor',NULL,NULL,42,NULL,'1234567890',1),(30,'doctor',NULL,NULL,43,NULL,'9676631289',1),(31,'doctor',NULL,NULL,44,NULL,'8297661566',1),(32,'doctor',NULL,NULL,45,NULL,'+917330699574',1);
/*!40000 ALTER TABLE `api_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_report`
--

DROP TABLE IF EXISTS `api_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_report` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `report_type` varchar(100) NOT NULL,
  `file_url` varchar(200) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `patient_id` bigint NOT NULL,
  `uploaded_by_id` int DEFAULT NULL,
  `file_size_bytes` int NOT NULL,
  `title` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_report_patient_id_061faea2_fk_api_patient_id` (`patient_id`),
  KEY `api_report_uploaded_by_id_c474045a_fk_auth_user_id` (`uploaded_by_id`),
  CONSTRAINT `api_report_patient_id_061faea2_fk_api_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `api_patient` (`id`),
  CONSTRAINT `api_report_uploaded_by_id_c474045a_fk_auth_user_id` FOREIGN KEY (`uploaded_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_report`
--

LOCK TABLES `api_report` WRITE;
/*!40000 ALTER TABLE `api_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_securitysetting`
--

DROP TABLE IF EXISTS `api_securitysetting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_securitysetting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `two_factor_auth` tinyint(1) NOT NULL,
  `biometric_login` tinyint(1) NOT NULL,
  `session_timeout_minutes` int NOT NULL,
  `pin_last_changed` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `api_securitysetting_user_id_c9cb8ed0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_securitysetting`
--

LOCK TABLES `api_securitysetting` WRITE;
/*!40000 ALTER TABLE `api_securitysetting` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_securitysetting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_supportticket`
--

DROP TABLE IF EXISTS `api_supportticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_supportticket` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subject` varchar(200) NOT NULL,
  `message` longtext NOT NULL,
  `status` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_supportticket_user_id_90e3da4c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_supportticket_user_id_90e3da4c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_supportticket`
--

LOCK TABLES `api_supportticket` WRITE;
/*!40000 ALTER TABLE `api_supportticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_supportticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_vitalsign`
--

DROP TABLE IF EXISTS `api_vitalsign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_vitalsign` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `timestamp` datetime(6) NOT NULL,
  `heart_rate` double DEFAULT NULL,
  `spo2` double DEFAULT NULL,
  `respiratory_rate` double DEFAULT NULL,
  `blood_pressure_sys` double DEFAULT NULL,
  `blood_pressure_dia` double DEFAULT NULL,
  `temperature` double DEFAULT NULL,
  `device_id` bigint DEFAULT NULL,
  `patient_id` bigint NOT NULL,
  `fio2` double DEFAULT NULL,
  `ie_ratio` varchar(20) DEFAULT NULL,
  `peep` double DEFAULT NULL,
  `ppeak` double DEFAULT NULL,
  `vte` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_vitalsign_device_id_2f6b4d02_fk_api_device_id` (`device_id`),
  KEY `api_vitalsign_patient_id_939a7237_fk_api_patient_id` (`patient_id`),
  CONSTRAINT `api_vitalsign_device_id_2f6b4d02_fk_api_device_id` FOREIGN KEY (`device_id`) REFERENCES `api_device` (`id`),
  CONSTRAINT `api_vitalsign_patient_id_939a7237_fk_api_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `api_patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_vitalsign`
--

LOCK TABLES `api_vitalsign` WRITE;
/*!40000 ALTER TABLE `api_vitalsign` DISABLE KEYS */;
INSERT INTO `api_vitalsign` VALUES (41,'2026-03-11 09:24:49.852287',108,91,24,124,75,37.08577426152677,41,44,70,NULL,NULL,NULL,416),(42,'2026-03-11 09:24:49.869446',77,96,16,117,76,36.97164479456984,42,45,21,NULL,NULL,NULL,450),(43,'2026-03-11 09:24:49.885653',119,99,15,101,55,39.31075560618749,43,46,40,NULL,NULL,NULL,450),(44,'2026-03-11 09:24:49.899033',66,92,14,109,80,37.14503645835842,44,47,35,NULL,NULL,NULL,450),(45,'2026-03-11 09:24:49.914657',76,93,21,118,75,39.27451562505317,45,48,40,NULL,NULL,NULL,450),(46,'2026-03-11 09:24:49.928748',76,98,14,125,82,37.020154681622714,46,49,21,NULL,NULL,NULL,450),(47,'2026-03-11 09:24:49.942848',79,89,22,121,84,37.103709371807916,47,50,30,NULL,NULL,NULL,450),(48,'2026-03-11 09:24:49.957886',76,98,14,125,83,36.61921529256386,48,51,21,NULL,NULL,NULL,450),(49,'2026-03-11 09:24:49.972450',76,96,14,117,82,36.62024403913785,49,52,21,NULL,NULL,NULL,450),(50,'2026-03-11 09:24:49.984781',75,96,17,123,76,36.74122502905039,50,53,21,NULL,NULL,NULL,450),(51,'2026-03-11 09:24:50.000067',74,99,15,151,105,36.65569394152316,51,54,21,NULL,NULL,NULL,450),(52,'2026-03-11 09:24:50.012965',84,96,14,121,84,37.132468125466254,52,55,21,NULL,NULL,NULL,450),(53,'2026-03-11 09:24:50.026725',90,99,14,120,84,36.68416373361384,53,56,21,NULL,NULL,NULL,450),(54,'2026-03-11 09:24:50.039178',82,97,17,121,85,36.73514043889659,54,57,21,NULL,NULL,NULL,450),(55,'2026-03-11 09:24:50.053483',90,99,16,118,83,37.177980895473176,55,58,21,NULL,NULL,NULL,450),(56,'2026-03-11 09:24:50.064853',90,99,18,120,84,37.19189090952152,56,59,21,NULL,NULL,NULL,450),(57,'2026-03-11 09:24:50.078093',78,99,15,119,82,36.931042040426426,57,60,21,NULL,NULL,NULL,450),(58,'2026-03-11 09:24:50.090558',70,99,18,118,79,36.62013564979973,58,61,21,NULL,NULL,NULL,450),(59,'2026-03-11 09:24:50.103049',83,98,16,125,80,37.10818490182325,59,62,21,NULL,NULL,NULL,450),(60,'2026-03-11 09:24:50.116396',87,99,14,119,82,37.063307912624666,60,63,21,NULL,NULL,NULL,450);
/*!40000 ALTER TABLE `api_vitalsign` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Token',7,'add_token'),(26,'Can change Token',7,'change_token'),(27,'Can delete Token',7,'delete_token'),(28,'Can view Token',7,'view_token'),(29,'Can add Token',8,'add_tokenproxy'),(30,'Can change Token',8,'change_tokenproxy'),(31,'Can delete Token',8,'delete_tokenproxy'),(32,'Can view Token',8,'view_tokenproxy'),(33,'Can add patient',9,'add_patient'),(34,'Can change patient',9,'change_patient'),(35,'Can delete patient',9,'delete_patient'),(36,'Can view patient',9,'view_patient'),(37,'Can add device',10,'add_device'),(38,'Can change device',10,'change_device'),(39,'Can delete device',10,'delete_device'),(40,'Can view device',10,'view_device'),(41,'Can add alert',11,'add_alert'),(42,'Can change alert',11,'change_alert'),(43,'Can delete alert',11,'delete_alert'),(44,'Can view alert',11,'view_alert'),(45,'Can add patient history',12,'add_patienthistory'),(46,'Can change patient history',12,'change_patienthistory'),(47,'Can delete patient history',12,'delete_patienthistory'),(48,'Can view patient history',12,'view_patienthistory'),(49,'Can add profile',13,'add_profile'),(50,'Can change profile',13,'change_profile'),(51,'Can delete profile',13,'delete_profile'),(52,'Can view profile',13,'view_profile'),(53,'Can add report',14,'add_report'),(54,'Can change report',14,'change_report'),(55,'Can delete report',14,'delete_report'),(56,'Can view report',14,'view_report'),(57,'Can add vital sign',15,'add_vitalsign'),(58,'Can change vital sign',15,'change_vitalsign'),(59,'Can delete vital sign',15,'delete_vitalsign'),(60,'Can view vital sign',15,'view_vitalsign'),(61,'Can add ai chat message',16,'add_aichatmessage'),(62,'Can change ai chat message',16,'change_aichatmessage'),(63,'Can delete ai chat message',16,'delete_aichatmessage'),(64,'Can view ai chat message',16,'view_aichatmessage'),(65,'Can add ai predicted event',17,'add_aipredictedevent'),(66,'Can change ai predicted event',17,'change_aipredictedevent'),(67,'Can delete ai predicted event',17,'delete_aipredictedevent'),(68,'Can view ai predicted event',17,'view_aipredictedevent'),(69,'Can add patient risk',18,'add_patientrisk'),(70,'Can change patient risk',18,'change_patientrisk'),(71,'Can delete patient risk',18,'delete_patientrisk'),(72,'Can view patient risk',18,'view_patientrisk'),(73,'Can add alert setting',19,'add_alertsetting'),(74,'Can change alert setting',19,'change_alertsetting'),(75,'Can delete alert setting',19,'delete_alertsetting'),(76,'Can view alert setting',19,'view_alertsetting'),(77,'Can add anomaly',20,'add_anomaly'),(78,'Can change anomaly',20,'change_anomaly'),(79,'Can delete anomaly',20,'delete_anomaly'),(80,'Can view anomaly',20,'view_anomaly'),(81,'Can add appearance setting',21,'add_appearancesetting'),(82,'Can change appearance setting',21,'change_appearancesetting'),(83,'Can delete appearance setting',21,'delete_appearancesetting'),(84,'Can view appearance setting',21,'view_appearancesetting'),(85,'Can add faq',22,'add_faq'),(86,'Can change faq',22,'change_faq'),(87,'Can delete faq',22,'delete_faq'),(88,'Can view faq',22,'view_faq'),(89,'Can add support ticket',23,'add_supportticket'),(90,'Can change support ticket',23,'change_supportticket'),(91,'Can delete support ticket',23,'delete_supportticket'),(92,'Can view support ticket',23,'view_supportticket'),(93,'Can add notification',24,'add_notification'),(94,'Can change notification',24,'change_notification'),(95,'Can delete notification',24,'delete_notification'),(96,'Can view notification',24,'view_notification'),(97,'Can add login history',25,'add_loginhistory'),(98,'Can change login history',25,'change_loginhistory'),(99,'Can delete login history',25,'delete_loginhistory'),(100,'Can view login history',25,'view_loginhistory'),(101,'Can add security setting',26,'add_securitysetting'),(102,'Can change security setting',26,'change_securitysetting'),(103,'Can delete security setting',26,'delete_securitysetting'),(104,'Can view security setting',26,'view_securitysetting'),(105,'Can add onboarding step',27,'add_onboardingstep'),(106,'Can change onboarding step',27,'change_onboardingstep'),(107,'Can delete onboarding step',27,'delete_onboardingstep'),(108,'Can view onboarding step',27,'view_onboardingstep'),(109,'Can add otp',28,'add_otp'),(110,'Can change otp',28,'change_otp'),(111,'Can delete otp',28,'delete_otp'),(112,'Can view otp',28,'view_otp'),(113,'Can add audit log',29,'add_auditlog'),(114,'Can change audit log',29,'change_auditlog'),(115,'Can delete audit log',29,'delete_auditlog'),(116,'Can view audit log',29,'view_auditlog');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (12,'pbkdf2_sha256$1000000$Wcos3CGrJZFM6pFpVBK7q6$Bp/++BR9bHvTKxpw44v47I9C1fIMdL5QHD/TSr2JFcw=','2026-03-28 04:46:02.633574',1,'admin','','','admin@admin.com',1,1,'2026-03-18 19:58:48.983810'),(13,'pbkdf2_sha256$1000000$7qAuse54ne3Y8VXfH7YMOT$usg/yd9p8sWU986ec/gQH3zvR1un2K+2oyAcjAmIkC4=',NULL,1,'brahmarreddy','','Brahma Reddy','brahmarreddy12@gmail.com',1,1,'2026-03-18 20:00:23.291687'),(36,'pbkdf2_sha256$1000000$EsrSQROuixifdAV8cNFBZP$vlzGEeLLFmM9hSqBB7sS+Xf6I4PTk2khRPK/CjuUJTw=',NULL,0,'yathakuntabrahmareddy1115@gmail.com','Dr','Brahma Reddy','yathakuntabrahmareddy1115@gmail.com',0,1,'2026-03-25 03:40:01.479661'),(37,'pbkdf2_sha256$1000000$SxpJJ1bEitRgGOPciJfEh9$0Ey19hyNBonIEsIgq7dRYRsWOZBE16RJrWhGP9jEg1s=',NULL,0,'yeruvanagalakshmi11@gmail.com','Dr','Naga','yeruvanagalakshmi11@gmail.com',0,1,'2026-03-25 03:48:21.100423'),(38,'pbkdf2_sha256$1000000$TvQfQsm7CUMHfgAubOwq6w$JPC1WNVierp6nO/IODxQ2XoWJ6fD/errXOCflFpnuEY=',NULL,0,'yathakuntabrahmareddy4070.sse@saveetha.com','Dr','karthik','yathakuntabrahmareddy4070.sse@saveetha.com',0,1,'2026-03-25 04:15:17.385634'),(40,'pbkdf2_sha256$1000000$VU32n6PfbL0JmWtAXezmnV$o8Gx+waepovryZY9KzBLLMNgmK0z/OCCq77scr8Efno=',NULL,0,'abhi12@gmail.com','Dr','abhi','abhi12@gmail.com',0,1,'2026-03-28 04:19:42.752345'),(41,'pbkdf2_sha256$1000000$Ej12lG9e4cTyQvrmbJapmp$yVW+IYSIFBzhD2J30G5G1KhP/uVleyl6pG6NF4IvetU=',NULL,0,'test_pending_user','','','test@example.com',0,1,'2026-03-28 04:33:00.422611'),(42,'pbkdf2_sha256$1000000$LKJ57KoAHCZWgrq2UXU3lB$bVoGNTgqoQyafSpApbHjF4px+QiNYO6R8z/xGanLttM=',NULL,0,'admin@gmail.com','Admin','','admin@gmail.com',0,1,'2026-03-28 04:44:33.358944'),(43,'pbkdf2_sha256$1000000$rUGWNKLm84mht4BOw9QUBI$cm7r6KIkGc9XXwZACJaYClAoX9KWel2U8LsOZGb2n1Y=',NULL,0,'kush234@gmail.com','Dr','kush','kush234@gmail.com',0,1,'2026-03-31 09:07:09.498998'),(44,'pbkdf2_sha256$1000000$HpXPfH69nkPxbEJInFvnMz$sFMFkN0VncWX/1H/1dJAmTOOIJjwvTexWRLWW58JArk=',NULL,0,'ram12@gmail.com','Dr','ramanji','ram12@gmail.com',0,1,'2026-04-01 08:00:37.719874'),(45,'pbkdf2_sha256$1000000$4eNNV6FO9oMP6sAMaje8b1$UuUM1rCp77s21K0/kdWghKFHYPbgIzhd3uR+SnMjGm0=',NULL,0,'kakumanisainithin@gmail.com','dr','nithin sai','kakumanisainithin@gmail.com',0,1,'2026-04-06 08:58:41.526384');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(16,'api','aichatmessage'),(17,'api','aipredictedevent'),(11,'api','alert'),(19,'api','alertsetting'),(20,'api','anomaly'),(21,'api','appearancesetting'),(29,'api','auditlog'),(10,'api','device'),(22,'api','faq'),(25,'api','loginhistory'),(24,'api','notification'),(27,'api','onboardingstep'),(28,'api','otp'),(9,'api','patient'),(12,'api','patienthistory'),(18,'api','patientrisk'),(13,'api','profile'),(14,'api','report'),(26,'api','securitysetting'),(23,'api','supportticket'),(15,'api','vitalsign'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(7,'authtoken','token'),(8,'authtoken','tokenproxy'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-03-09 04:15:56.765674'),(2,'auth','0001_initial','2026-03-09 04:15:57.327773'),(3,'admin','0001_initial','2026-03-09 04:15:57.467177'),(4,'admin','0002_logentry_remove_auto_add','2026-03-09 04:15:57.472051'),(5,'admin','0003_logentry_add_action_flag_choices','2026-03-09 04:15:57.477267'),(6,'api','0001_initial','2026-03-09 04:15:58.336313'),(7,'api','0002_aichatmessage','2026-03-09 04:15:58.422754'),(8,'api','0003_aipredictedevent_delete_aianalysis','2026-03-09 04:15:58.521979'),(9,'api','0004_patientrisk','2026-03-09 04:15:58.605480'),(10,'api','0005_alert_ai_confidence_alert_current_value_and_more','2026-03-09 04:15:58.886486'),(11,'api','0006_alertsetting','2026-03-09 04:15:58.993341'),(12,'api','0007_anomaly','2026-03-09 04:15:59.079611'),(13,'api','0008_appearancesetting','2026-03-09 04:15:59.193838'),(14,'api','0009_faq_supportticket','2026-03-09 04:15:59.307505'),(15,'api','0010_vitalsign_fio2_vitalsign_ie_ratio_vitalsign_peep_and_more','2026-03-09 04:15:59.593431'),(16,'api','0011_notification','2026-03-09 04:15:59.702809'),(17,'api','0012_remove_patienthistory_diagnosis_and_more','2026-03-09 04:16:00.036420'),(18,'api','0013_profile_employee_id_profile_phone_number','2026-03-09 04:16:00.131731'),(19,'api','0014_report_file_size_bytes_report_title_and_more','2026-03-09 04:16:00.283289'),(20,'api','0015_loginhistory_securitysetting','2026-03-09 04:16:00.477353'),(21,'api','0016_onboardingstep','2026-03-09 04:16:00.501531'),(22,'api','0017_otp','2026-03-09 04:16:00.526476'),(23,'contenttypes','0002_remove_content_type_name','2026-03-09 04:16:00.651127'),(24,'auth','0002_alter_permission_name_max_length','2026-03-09 04:16:00.725040'),(25,'auth','0003_alter_user_email_max_length','2026-03-09 04:16:00.760481'),(26,'auth','0004_alter_user_username_opts','2026-03-09 04:16:00.770523'),(27,'auth','0005_alter_user_last_login_null','2026-03-09 04:16:00.850939'),(28,'auth','0006_require_contenttypes_0002','2026-03-09 04:16:00.853191'),(29,'auth','0007_alter_validators_add_error_messages','2026-03-09 04:16:00.862311'),(30,'auth','0008_alter_user_username_max_length','2026-03-09 04:16:00.942399'),(31,'auth','0009_alter_user_last_name_max_length','2026-03-09 04:16:01.019487'),(32,'auth','0010_alter_group_name_max_length','2026-03-09 04:16:01.039797'),(33,'auth','0011_update_proxy_permissions','2026-03-09 04:16:01.052837'),(34,'auth','0012_alter_user_first_name_max_length','2026-03-09 04:16:01.131746'),(35,'authtoken','0001_initial','2026-03-09 04:16:01.241593'),(36,'authtoken','0002_auto_20160226_1747','2026-03-09 04:16:01.278286'),(37,'authtoken','0003_tokenproxy','2026-03-09 04:16:01.281283'),(38,'authtoken','0004_alter_tokenproxy_options','2026-03-09 04:16:01.284528'),(39,'sessions','0001_initial','2026-03-09 04:16:01.317158'),(40,'api','0018_profile_is_approved','2026-03-18 19:58:39.812973'),(41,'api','0019_notification_target_user_id_alter_notification_title','2026-03-18 20:09:06.235333'),(42,'api','0020_auditlog','2026-03-26 04:09:33.295237');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('aw51018tkn3c6pxjz6r7q4tncfn4hhom','.eJxVjMsOwiAUBf-FtSGFAuW6dO83ELgPqZqS9LEy_rs26UK3Z2bOS6W8rTVtC89pJHVWxqrT71gyPnjaCd3zdGsa27TOY9G7og-66Gsjfl4O9--g5qV-a-mo54GKD0KBPfQRfKEhOgOdCEg0LsRoBJgjFkCCwXaIEMT5ghbU-wMXtjhz:1w6LYg:agH_enjRk0_DkvoNXFwBGXNSb1wDwqDJp2g_Ywgll9o','2026-04-11 04:46:02.645001');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-09  8:31:39
