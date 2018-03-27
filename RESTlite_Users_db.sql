CREATE DATABASE  IF NOT EXISTS `RESTlite_Users_db` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
USE `RESTlite_Users_db`;
-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: 127.0.0.1    Database: RESTlite_Users_db
-- ------------------------------------------------------
-- Server version	5.7.21

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
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message_id` int(11) NOT NULL,
  `comment` longtext COLLATE utf8_bin NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_comments_user_idx` (`user_id`),
  KEY `fk_comments_message_idx` (`message_id`),
  CONSTRAINT `fk_comments_message` FOREIGN KEY (`message_id`) REFERENCES `messages` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `fk_comments_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (1,1,1,'This is the first real comment.','2018-03-27 13:36:01',NULL),(2,2,2,'Four score and seven years ago our forefathers brought forth on this continent an new concept conceived in liberty.','2018-03-27 13:37:42',NULL),(3,4,1,'I think you can come up with a better quote than that Andrew.','2018-03-27 13:44:48',NULL),(4,6,2,'This is for all my ninjas.','2018-03-27 14:31:26',NULL),(5,6,4,'I voted for you... I just want you to know this.','2018-03-27 14:49:02',NULL),(6,6,3,'Just want to make sure comment is still working.','2018-03-27 17:49:55',NULL),(7,1,6,'Test personal wall comments.','2018-03-27 19:14:43',NULL),(10,2,4,'I need to make sure that the main wall is still working correctly.','2018-03-27 19:48:39',NULL);
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` longtext COLLATE utf8_bin NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,'Its day one again at the POst.','2018-03-27 12:52:39',NULL),(2,'Here is my second message for testing.','2018-03-27 12:56:52',NULL),(3,'Test again.','2018-03-27 13:35:49',NULL),(4,'You know what time it is...im back. And American will be great again.','2018-03-27 13:39:27',NULL),(5,'Once personal wall messages and comments are functional, this branch will get merged with the branch dev.','2018-03-27 14:32:20',NULL),(6,'To test personal wall posts','2018-03-27 14:33:20',NULL),(7,'You could learn a thing or two from me.  If you want to live forever that is.','2018-03-27 19:24:06',NULL),(8,'We have never met but I think we have much in common.  How about coffee tomorrow?','2018-03-27 19:37:53',NULL),(9,'This is all to test a mans will and commitment.','2018-03-27 19:49:46',NULL),(10,'Note to self, need to sort main wall messages by date.','2018-03-27 19:50:36',NULL);
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) COLLATE utf8_bin NOT NULL,
  `last_name` varchar(45) COLLATE utf8_bin NOT NULL,
  `email` varchar(60) COLLATE utf8_bin NOT NULL,
  `password` varchar(32) COLLATE utf8_bin NOT NULL,
  `salt` varchar(33) COLLATE utf8_bin NOT NULL,
  `birthdate` datetime NOT NULL,
  `permission_level` int(5) NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Andrew','Williams','mawfia@yahoo.com','6101c312c0b1714711558b47cbc89d11','99487600d4e0dec9b22b490cfca6cd','1985-03-06 00:00:00',3,'2018-03-03 00:42:40','2018-03-27 19:12:34'),(2,'Abraham','Lincoln','a.lincoln@whitehouse.gov','9f1e807c23c612170f32cb1bc8b5cf9b','71cb46ee11e09d050218e0341c035e','1976-02-06 00:00:00',2,'2018-03-03 17:56:54','2018-03-27 19:23:35'),(4,'Donald','Trump','dtrump@whitehouse.gov','6ea97158f2977b61fdab62dffe9d7398','f3cfab506b0f95db0b81c699335ecf','1972-01-01 00:00:00',1,'2018-03-04 04:36:21','2018-03-27 19:49:15'),(6,'Daren','Danvey','Danzy@DanzyLove.com','32669612c754ee716451894d1a294d70','51e8e21b42aa46b846634157d8e5c1','1977-01-21 00:00:00',3,'2018-03-04 16:17:13','2018-03-27 14:31:09');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_messages`
--

DROP TABLE IF EXISTS `users_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(5) NOT NULL,
  `message_id` int(5) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_users_messages_idx` (`message_id`),
  KEY `fk_messages_users_idx` (`user_id`),
  CONSTRAINT `fk_messages_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_messages` FOREIGN KEY (`message_id`) REFERENCES `messages` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_messages`
--

LOCK TABLES `users_messages` WRITE;
/*!40000 ALTER TABLE `users_messages` DISABLE KEYS */;
INSERT INTO `users_messages` VALUES (1,1,1),(2,1,2),(3,1,3),(4,4,4),(5,6,5),(6,2,6),(7,1,6),(8,2,7),(9,4,7),(10,2,8),(11,6,8),(12,4,9),(13,4,10),(14,4,10);
/*!40000 ALTER TABLE `users_messages` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-03-27 19:59:04
