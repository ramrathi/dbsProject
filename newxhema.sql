-- MySQL dump 10.13  Distrib 5.7.26, for Linux (x86_64)
--
-- Host: localhost    Database: dbsproject
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
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
-- Dumping data for table `Attending`
--

LOCK TABLES `Attending` WRITE;
/*!40000 ALTER TABLE `Attending` DISABLE KEYS */;
INSERT INTO `Attending` VALUES (1,3),(1,5),(1,8);
/*!40000 ALTER TABLE `Attending` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `Belongs`
--

LOCK TABLES `Belongs` WRITE;
/*!40000 ALTER TABLE `Belongs` DISABLE KEYS */;
/*!40000 ALTER TABLE `Belongs` ENABLE KEYS */;
UNLOCK TABLES;

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
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`comm_id`),
  KEY `Comments_fk0` (`post_id`),
  KEY `Comments_fk1` (`user_id`),
  CONSTRAINT `Comments_fk0` FOREIGN KEY (`post_id`) REFERENCES `Posts` (`p_id`),
  CONSTRAINT `Comments_fk1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Comments`
--

LOCK TABLES `Comments` WRITE;
/*!40000 ALTER TABLE `Comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `Comments` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Community`
--

LOCK TABLES `Community` WRITE;
/*!40000 ALTER TABLE `Community` DISABLE KEYS */;
/*!40000 ALTER TABLE `Community` ENABLE KEYS */;
UNLOCK TABLES;

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
  `media` tinyblob,
  `mediasrc` varchar(2550) DEFAULT NULL,
  PRIMARY KEY (`e_id`),
  KEY `Events_fk0` (`host`),
  CONSTRAINT `Events_fk0` FOREIGN KEY (`host`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Events`
--

LOCK TABLES `Events` WRITE;
/*!40000 ALTER TABLE `Events` DISABLE KEYS */;
INSERT INTO `Events` VALUES (1,5,'Manipal','PARTYYY',NULL,'img/logo.png');
/*!40000 ALTER TABLE `Events` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `Friends`
--

LOCK TABLES `Friends` WRITE;
/*!40000 ALTER TABLE `Friends` DISABLE KEYS */;
INSERT INTO `Friends` VALUES (5,1),(8,1),(1,5),(1,8);
/*!40000 ALTER TABLE `Friends` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Market`
--

LOCK TABLES `Market` WRITE;
/*!40000 ALTER TABLE `Market` DISABLE KEYS */;
INSERT INTO `Market` VALUES (1,'Fridge','Cools your food for you, requires electricity',10000,5,0),(2,'Guitar','Cort CR100, Mint condition',15000,5,0),(3,'Induction cooker','New induction, heats up and cooks food',1000,8,0),(4,'My life','Take my life',10,1,1);
/*!40000 ALTER TABLE `Market` ENABLE KEYS */;
UNLOCK TABLES;

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
  `media` blob,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`m_id`),
  KEY `Messages_fk0` (`From`),
  KEY `Messages_fk1` (`To`),
  CONSTRAINT `Messages_fk0` FOREIGN KEY (`From`) REFERENCES `Users` (`id`),
  CONSTRAINT `Messages_fk1` FOREIGN KEY (`To`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Messages`
--

LOCK TABLES `Messages` WRITE;
/*!40000 ALTER TABLE `Messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `Messages` ENABLE KEYS */;
UNLOCK TABLES;

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
  `price` int(10) NOT NULL,
  PRIMARY KEY (`s_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Music`
--

LOCK TABLES `Music` WRITE;
/*!40000 ALTER TABLE `Music` DISABLE KEYS */;
/*!40000 ALTER TABLE `Music` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `Payment`
--

LOCK TABLES `Payment` WRITE;
/*!40000 ALTER TABLE `Payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `Payment` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `Playlist`
--

LOCK TABLES `Playlist` WRITE;
/*!40000 ALTER TABLE `Playlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `Playlist` ENABLE KEYS */;
UNLOCK TABLES;

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
  `time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `photo` varchar(2550) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  `community` int(10) DEFAULT NULL,
  `photosrc` varchar(2550) DEFAULT NULL,
  PRIMARY KEY (`p_id`),
  KEY `Posts_fk0` (`u_id`),
  KEY `Posts_fk1` (`community`),
  CONSTRAINT `Posts_fk0` FOREIGN KEY (`u_id`) REFERENCES `Users` (`id`),
  CONSTRAINT `Posts_fk1` FOREIGN KEY (`community`) REFERENCES `Community` (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Posts`
--

LOCK TABLES `Posts` WRITE;
/*!40000 ALTER TABLE `Posts` DISABLE KEYS */;
INSERT INTO `Posts` VALUES (1,1,'asdf','2019-10-13 19:13:53',NULL,NULL,NULL,NULL),(2,1,'This should work','2019-10-13 19:17:08',NULL,NULL,NULL,NULL),(3,1,'hello hello hello','2019-10-13 19:27:39',NULL,NULL,NULL,NULL),(4,1,'This is my new post','2019-10-13 19:29:38',NULL,NULL,NULL,NULL),(24,8,'This is a penguin!','2019-10-26 18:37:38',NULL,NULL,NULL,'static/1000x-1.jpg'),(26,1,'LMAOOOOO','2019-10-26 18:42:52',NULL,NULL,NULL,'static/x.jpg'),(28,1,'F ','2019-10-26 20:26:14',NULL,NULL,NULL,'static/meme.jpg');
/*!40000 ALTER TABLE `Posts` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `Requests`
--

LOCK TABLES `Requests` WRITE;
/*!40000 ALTER TABLE `Requests` DISABLE KEYS */;
INSERT INTO `Requests` VALUES (8,5),(1,3);
/*!40000 ALTER TABLE `Requests` ENABLE KEYS */;
UNLOCK TABLES;

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
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `message` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`t_id`),
  KEY `Transactions_fk0` (`from`),
  KEY `Transactions_fk1` (`to`),
  CONSTRAINT `Transactions_fk0` FOREIGN KEY (`from`) REFERENCES `Users` (`id`),
  CONSTRAINT `Transactions_fk1` FOREIGN KEY (`to`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Transactions`
--

LOCK TABLES `Transactions` WRITE;
/*!40000 ALTER TABLE `Transactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `Transactions` ENABLE KEYS */;
UNLOCK TABLES;

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
  `wallet` int(10) NOT NULL DEFAULT '50',
  `picture` varchar(2550) NOT NULL DEFAULT 'https://i.pinimg.com/236x/fc/38/ae/fc38ae834ebfc2456a0906dfa4c56163--say-to-dramas.jpg',
  PRIMARY KEY (`id`),
  UNIQUE KEY `wallet` (`wallet`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'Ram Rathi','hello','1999-03-02',1,'Fuck you','pune','india','ram@ram','9999999',-31000,'https://scontent.fbom2-1.fna.fbcdn.net/v/t1.0-9/20800338_1612121165488974_8186128540972407853_n.jpg?_nc_cat=108&_nc_oc=AQks8IhCAON-sQwtUyTMEpE97j13qJsqbKvZOgKQgFcqIgyTsRUoykCZiJOtAZ_9Kpw&_nc_ht=scontent.fbom2-1.fna&oh=21013c69416344515c547a9f9d1f440e&oe=5E25A624'),(3,'ram','hello','1999-03-02',1,NULL,NULL,NULL,'hello',NULL,1,'https://i.pinimg.com/236x/fc/38/ae/fc38ae834ebfc2456a0906dfa4c56163--say-to-dramas.jpg'),(5,'sourav','adfaddfa','1999-05-27',1,NULL,NULL,NULL,'s@s',NULL,85229,'https://i.pinimg.com/236x/fc/38/ae/fc38ae834ebfc2456a0906dfa4c56163--say-to-dramas.jpg'),(6,'s','asdf','1999-05-27',1,NULL,NULL,NULL,'sdaf',NULL,22405,'https://i.pinimg.com/236x/fc/38/ae/fc38ae834ebfc2456a0906dfa4c56163--say-to-dramas.jpg'),(7,'asdf','asdf','1999-05-27',1,NULL,NULL,NULL,'adf',NULL,77045,'https://i.pinimg.com/236x/fc/38/ae/fc38ae834ebfc2456a0906dfa4c56163--say-to-dramas.jpg'),(8,'faizaan','hello','1999-05-27',1,'Hi im faizu',NULL,NULL,'faizaan@faizaan',NULL,102,'http://4.bp.blogspot.com/-jj13PvJtPqY/Totq30ND_KI/AAAAAAAABHI/ZnUWkQKO22Q/s1600/batman-for-facebook.jpg'),(9,'sourav2999','fuckyouram','1999-05-27',1,NULL,NULL,NULL,'souravagrawal.1023@gmail.com',NULL,96038,'https://i.pinimg.com/236x/fc/38/ae/fc38ae834ebfc2456a0906dfa4c56163--say-to-dramas.jpg');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-10-31 17:56:40
