CREATE DATABASE IF NOT EXISTS fccr;

USE fccr;

CREATE TABLE IF NOT EXISTS groups (
    username VARCHAR(65) NOT NULL UNIQUE PRIMARY KEY,
    usertype VARCHAR(65) NOT NULL DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS users (
    username  VARCHAR(65)  NOT NULL UNIQUE PRIMARY KEY,
    pass_word VARCHAR(767) NOT NULL,
    FOREIGN KEY fk_username(username) REFERENCES groups (username)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS services (
    usertype  VARCHAR(65)  NOT NULL UNIQUE PRIMARY KEY,
    service VARCHAR(767) NOT NULL
);

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES ('usertype1','accessGranted'),('usertype2','accessDenied');
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;




