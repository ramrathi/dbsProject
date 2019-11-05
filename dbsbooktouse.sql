-- MariaDB dump 10.17  Distrib 10.4.8-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: dbsproject
-- ------------------------------------------------------
-- Server version	10.4.8-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Attending`
--

DROP TABLE IF EXISTS `Attending`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Attending` (
  `event_id` int(10) NOT NULL,
  `user_id` int(10) NOT NULL,
  PRIMARY KEY (`event_id`,`user_id`),
  KEY `Attending_fk1` (`user_id`),
  CONSTRAINT `Attending_fk0` FOREIGN KEY (`event_id`) REFERENCES `Events` (`e_id`),
  CONSTRAINT `Attending_fk1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Belongs`
--

DROP TABLE IF EXISTS `Belongs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Belongs` (
  `user_id` int(10) NOT NULL,
  `community_id` int(10) NOT NULL,
  PRIMARY KEY (`user_id`,`community_id`),
  KEY `Belongs_fk1` (`community_id`),
  CONSTRAINT `Belongs_fk0` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`),
  CONSTRAINT `Belongs_fk1` FOREIGN KEY (`community_id`) REFERENCES `Community` (`c_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Comments`
--

DROP TABLE IF EXISTS `Comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Comments` (
  `comm_id` int(10) NOT NULL AUTO_INCREMENT,
  `post_id` int(10) NOT NULL,
  `user_id` int(10) NOT NULL,
  `content` varchar(255) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`comm_id`),
  KEY `Comments_fk0` (`post_id`),
  KEY `Comments_fk1` (`user_id`),
  CONSTRAINT `Comments_fk0` FOREIGN KEY (`post_id`) REFERENCES `Posts` (`p_id`),
  CONSTRAINT `Comments_fk1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Community`
--

DROP TABLE IF EXISTS `Community`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Community` (
  `c_id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Events`
--

DROP TABLE IF EXISTS `Events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Events` (
  `e_id` int(10) NOT NULL AUTO_INCREMENT,
  `host` int(10) NOT NULL,
  `location` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `media` tinyblob DEFAULT NULL,
  `mediasrc` varchar(2550) DEFAULT NULL,
  PRIMARY KEY (`e_id`),
  KEY `Events_fk0` (`host`),
  CONSTRAINT `Events_fk0` FOREIGN KEY (`host`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 trigger eventgoing  after insert on Events  for each row begin  insert into Attending values (new.e_id, new.host);  end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Friends`
--

DROP TABLE IF EXISTS `Friends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Friends` (
  `u1_id` int(10) NOT NULL,
  `u2_id` int(10) NOT NULL,
  PRIMARY KEY (`u1_id`,`u2_id`),
  KEY `Friends_fk1` (`u2_id`),
  CONSTRAINT `Friends_fk0` FOREIGN KEY (`u1_id`) REFERENCES `Users` (`id`),
  CONSTRAINT `Friends_fk1` FOREIGN KEY (`u2_id`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Market`
--

DROP TABLE IF EXISTS `Market`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Market` (
  `i_id` int(10) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `price` int(10) DEFAULT NULL,
  `seller` int(10) NOT NULL,
  `sold` int(1) NOT NULL,
  PRIMARY KEY (`i_id`),
  KEY `Market_fk0` (`seller`),
  CONSTRAINT `Market_fk0` FOREIGN KEY (`seller`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Messages`
--

DROP TABLE IF EXISTS `Messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Messages` (
  `m_id` int(10) NOT NULL AUTO_INCREMENT,
  `From` int(10) NOT NULL,
  `To` int(10) NOT NULL,
  `Content` varchar(500) NOT NULL,
  `media` blob DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`m_id`),
  KEY `Messages_fk0` (`From`),
  KEY `Messages_fk1` (`To`),
  CONSTRAINT `Messages_fk0` FOREIGN KEY (`From`) REFERENCES `Users` (`id`),
  CONSTRAINT `Messages_fk1` FOREIGN KEY (`To`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Music`
--

DROP TABLE IF EXISTS `Music`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Music` (
  `s_id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `artist` varchar(50) NOT NULL,
  `album` varchar(50) DEFAULT NULL,
  `year` int(10) DEFAULT NULL,
  `link` varchar(30) NOT NULL,
  PRIMARY KEY (`s_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Payment`
--

DROP TABLE IF EXISTS `Payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Payment` (
  `user_id` int(10) NOT NULL,
  `item_id` int(10) NOT NULL,
  PRIMARY KEY (`user_id`,`item_id`),
  KEY `Payment_fk1` (`item_id`),
  CONSTRAINT `Payment_fk0` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`),
  CONSTRAINT `Payment_fk1` FOREIGN KEY (`item_id`) REFERENCES `Market` (`i_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Playlist`
--

DROP TABLE IF EXISTS `Playlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Playlist` (
  `user_id` int(10) NOT NULL,
  `song_id` int(10) NOT NULL,
  PRIMARY KEY (`user_id`,`song_id`),
  KEY `Playlist_fk1` (`song_id`),
  CONSTRAINT `Playlist_fk0` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`),
  CONSTRAINT `Playlist_fk1` FOREIGN KEY (`song_id`) REFERENCES `Music` (`s_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Posts`
--

DROP TABLE IF EXISTS `Posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Posts` (
  `p_id` int(10) NOT NULL AUTO_INCREMENT,
  `u_id` int(10) NOT NULL,
  `content` varchar(500) NOT NULL,
  `time_stamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `photo` varchar(2550) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  `community` int(10) DEFAULT NULL,
  `photosrc` varchar(2550) DEFAULT NULL,
  PRIMARY KEY (`p_id`),
  KEY `Posts_fk0` (`u_id`),
  KEY `Posts_fk1` (`community`),
  CONSTRAINT `Posts_fk0` FOREIGN KEY (`u_id`) REFERENCES `Users` (`id`),
  CONSTRAINT `Posts_fk1` FOREIGN KEY (`community`) REFERENCES `Community` (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Requests`
--

DROP TABLE IF EXISTS `Requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Requests` (
  `u_id1` int(10) NOT NULL,
  `u_id2` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Transactions`
--

DROP TABLE IF EXISTS `Transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Transactions` (
  `t_id` int(10) NOT NULL AUTO_INCREMENT,
  `from` int(10) NOT NULL,
  `to` int(10) NOT NULL,
  `money` int(10) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `message` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`t_id`),
  KEY `Transactions_fk0` (`from`),
  KEY `Transactions_fk1` (`to`),
  CONSTRAINT `Transactions_fk0` FOREIGN KEY (`from`) REFERENCES `Users` (`id`),
  CONSTRAINT `Transactions_fk1` FOREIGN KEY (`to`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `dob` date NOT NULL,
  `gender` int(1) NOT NULL,
  `bio` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `wallet` int(10) NOT NULL DEFAULT 50,
  `picture` varchar(2550) NOT NULL DEFAULT 'https://www.thehindu.com/sci-tech/technology/internet/article17759222.ece/ALTERNATES/FREE_960/02th-egg-person',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-05 22:46:43
