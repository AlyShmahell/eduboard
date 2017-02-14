-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 14, 2017 at 01:37 AM
-- Server version: 5.5.54-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.20

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `webtech`
--
CREATE DATABASE IF NOT EXISTS `webtech` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `webtech`;

-- --------------------------------------------------------

--
-- Table structure for table `a0693bd09e8214164198812ee85d9256cb36d7ab7`
--

CREATE TABLE IF NOT EXISTS `a0693bd09e8214164198812ee85d9256cb36d7ab7` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `a0693bd09e8214164198812ee85d9256cb36d7ab7`
--

INSERT INTO `a0693bd09e8214164198812ee85d9256cb36d7ab7` (`assetname`, `assetcoordinates`) VALUES
('HadroCannon', '8904.5904');

-- --------------------------------------------------------

--
-- Table structure for table `a8b008c0e213634241fdaec6c48992223e6b0a907`
--

CREATE TABLE IF NOT EXISTS `a8b008c0e213634241fdaec6c48992223e6b0a907` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `a8b008c0e213634241fdaec6c48992223e6b0a907`
--

INSERT INTO `a8b008c0e213634241fdaec6c48992223e6b0a907` (`assetname`, `assetcoordinates`) VALUES
('ModularGemFactory#06', '4890.4009');

-- --------------------------------------------------------

--
-- Table structure for table `a9b3e0d2d09f6a6bf4d0478c2d7b7ca3037b8d8b3`
--

CREATE TABLE IF NOT EXISTS `a9b3e0d2d09f6a6bf4d0478c2d7b7ca3037b8d8b3` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `a9b3e0d2d09f6a6bf4d0478c2d7b7ca3037b8d8b3`
--

INSERT INTO `a9b3e0d2d09f6a6bf4d0478c2d7b7ca3037b8d8b3` (`assetname`, `assetcoordinates`) VALUES
('Venus', '-1205.4560');

-- --------------------------------------------------------

--
-- Table structure for table `a18e4a64ed94efa7fd8c4c30d189028f1a0d355d2`
--

CREATE TABLE IF NOT EXISTS `a18e4a64ed94efa7fd8c4c30d189028f1a0d355d2` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `a18e4a64ed94efa7fd8c4c30d189028f1a0d355d2`
--

INSERT INTO `a18e4a64ed94efa7fd8c4c30d189028f1a0d355d2` (`assetname`, `assetcoordinates`) VALUES
('WideGalaxyUniversityOfAstronomy', '1709.2039');

-- --------------------------------------------------------

--
-- Table structure for table `a67f38592435a8b812cfd1f9e3520733230e95f1d`
--

CREATE TABLE IF NOT EXISTS `a67f38592435a8b812cfd1f9e3520733230e95f1d` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `a67f38592435a8b812cfd1f9e3520733230e95f1d`
--

INSERT INTO `a67f38592435a8b812cfd1f9e3520733230e95f1d` (`assetname`, `assetcoordinates`) VALUES
('IntergalacticPortal', '2000.2000');

-- --------------------------------------------------------

--
-- Table structure for table `a78ed61248d6afb7f3f77e5b3934fb7ae2ec177b5`
--

CREATE TABLE IF NOT EXISTS `a78ed61248d6afb7f3f77e5b3934fb7ae2ec177b5` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `a78ed61248d6afb7f3f77e5b3934fb7ae2ec177b5`
--

INSERT INTO `a78ed61248d6afb7f3f77e5b3934fb7ae2ec177b5` (`assetname`, `assetcoordinates`) VALUES
('AsteroidSet#9', '7894.8309');

-- --------------------------------------------------------

--
-- Table structure for table `a214eba40b105cef623ff0973b104b164c6f68da2`
--

CREATE TABLE IF NOT EXISTS `a214eba40b105cef623ff0973b104b164c6f68da2` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `a214eba40b105cef623ff0973b104b164c6f68da2`
--

INSERT INTO `a214eba40b105cef623ff0973b104b164c6f68da2` (`assetname`, `assetcoordinates`) VALUES
('Asteroid-EDGGC9', '6290.3404');

-- --------------------------------------------------------

--
-- Table structure for table `a629cddbc5b909dc5b2b7c84a743adc4d4386dfa5`
--

CREATE TABLE IF NOT EXISTS `a629cddbc5b909dc5b2b7c84a743adc4d4386dfa5` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `a629cddbc5b909dc5b2b7c84a743adc4d4386dfa5`
--

INSERT INTO `a629cddbc5b909dc5b2b7c84a743adc4d4386dfa5` (`assetname`, `assetcoordinates`) VALUES
('Pluto', '9007.1290');

-- --------------------------------------------------------

--
-- Table structure for table `a3636c53fa5e6cea7b6c94f73d18e4e9806ff8a35`
--

CREATE TABLE IF NOT EXISTS `a3636c53fa5e6cea7b6c94f73d18e4e9806ff8a35` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `a3636c53fa5e6cea7b6c94f73d18e4e9806ff8a35`
--

INSERT INTO `a3636c53fa5e6cea7b6c94f73d18e4e9806ff8a35` (`assetname`, `assetcoordinates`) VALUES
('GoogleSpaceStation', '1110.0940');

-- --------------------------------------------------------

--
-- Table structure for table `aae7f8c00449fdc6540f37ab31dec1bdfc4797767`
--

CREATE TABLE IF NOT EXISTS `aae7f8c00449fdc6540f37ab31dec1bdfc4797767` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `aae7f8c00449fdc6540f37ab31dec1bdfc4797767`
--

INSERT INTO `aae7f8c00449fdc6540f37ab31dec1bdfc4797767` (`assetname`, `assetcoordinates`) VALUES
('BeltObservatory#90', '9810.9324');

-- --------------------------------------------------------

--
-- Table structure for table `aafca71be6d4c59504dbea38a8653d6d38873d7cc`
--

CREATE TABLE IF NOT EXISTS `aafca71be6d4c59504dbea38a8653d6d38873d7cc` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `aafca71be6d4c59504dbea38a8653d6d38873d7cc`
--

INSERT INTO `aafca71be6d4c59504dbea38a8653d6d38873d7cc` (`assetname`, `assetcoordinates`) VALUES
('cometX41', '1398.2345'),
('cometX42', '1398.2370');

-- --------------------------------------------------------

--
-- Table structure for table `ab8fdd6503c8d616d33430f8e502b56fbff2d5d0a`
--

CREATE TABLE IF NOT EXISTS `ab8fdd6503c8d616d33430f8e502b56fbff2d5d0a` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ab8fdd6503c8d616d33430f8e502b56fbff2d5d0a`
--

INSERT INTO `ab8fdd6503c8d616d33430f8e502b56fbff2d5d0a` (`assetname`, `assetcoordinates`) VALUES
('Moon', '1939.3245');

-- --------------------------------------------------------

--
-- Table structure for table `ab98a94660075801eda3a72bc4bc26cff7d4d5749`
--

CREATE TABLE IF NOT EXISTS `ab98a94660075801eda3a72bc4bc26cff7d4d5749` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ab98a94660075801eda3a72bc4bc26cff7d4d5749`
--

INSERT INTO `ab98a94660075801eda3a72bc4bc26cff7d4d5749` (`assetname`, `assetcoordinates`) VALUES
('cometX39', '1382.2349'),
('cometX40', '1382.2369'),
('cometX70', '1382.2389'),
('cometX80', '1382.2410');

-- --------------------------------------------------------

--
-- Table structure for table `ac7fc60db621c5e505e152281daa6dd4c52ac6a3a`
--

CREATE TABLE IF NOT EXISTS `ac7fc60db621c5e505e152281daa6dd4c52ac6a3a` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ac7fc60db621c5e505e152281daa6dd4c52ac6a3a`
--

INSERT INTO `ac7fc60db621c5e505e152281daa6dd4c52ac6a3a` (`assetname`, `assetcoordinates`) VALUES
('Comet-Y19', '2890.4903');

-- --------------------------------------------------------

--
-- Table structure for table `acac24742ab3451466c86da435ff1fa64dc93b682`
--

CREATE TABLE IF NOT EXISTS `acac24742ab3451466c86da435ff1fa64dc93b682` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `acac24742ab3451466c86da435ff1fa64dc93b682`
--

INSERT INTO `acac24742ab3451466c86da435ff1fa64dc93b682` (`assetname`, `assetcoordinates`) VALUES
('JupiterStation#1', '4327.9010');

-- --------------------------------------------------------

--
-- Table structure for table `adf9969f90fecb40ce11624f40f6af9323ad16051`
--

CREATE TABLE IF NOT EXISTS `adf9969f90fecb40ce11624f40f6af9323ad16051` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `adf9969f90fecb40ce11624f40f6af9323ad16051`
--

INSERT INTO `adf9969f90fecb40ce11624f40f6af9323ad16051` (`assetname`, `assetcoordinates`) VALUES
('Mars', '6040.3040');

-- --------------------------------------------------------

--
-- Table structure for table `Administrator`
--

CREATE TABLE IF NOT EXISTS `Administrator` (
  `corporation` varchar(767) NOT NULL,
  `database_token` varchar(767) DEFAULT NULL,
  PRIMARY KEY (`corporation`),
  UNIQUE KEY `corporation` (`corporation`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `af65930a613b6ef323a920c1f6cbd0440c3ee0d80`
--

CREATE TABLE IF NOT EXISTS `af65930a613b6ef323a920c1f6cbd0440c3ee0d80` (
  `assetname` varchar(300) NOT NULL,
  `assetcoordinates` varchar(300) NOT NULL,
  PRIMARY KEY (`assetname`),
  UNIQUE KEY `assetname` (`assetname`),
  UNIQUE KEY `assetcoordinates` (`assetcoordinates`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `af65930a613b6ef323a920c1f6cbd0440c3ee0d80`
--

INSERT INTO `af65930a613b6ef323a920c1f6cbd0440c3ee0d80` (`assetname`, `assetcoordinates`) VALUES
('HannaH-Space-Luxury-Hotel', '3060.3450');

-- --------------------------------------------------------

--
-- Table structure for table `groups`
--

CREATE TABLE IF NOT EXISTS `groups` (
  `username` varchar(65) NOT NULL,
  `usertype` varchar(65) NOT NULL DEFAULT 'user',
  PRIMARY KEY (`username`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `groups`
--

INSERT INTO `groups` (`username`, `usertype`) VALUES
('AAGC', 'usertype1'),
('Administrator', 'admin'),
('AlyTech', 'usertype2'),
('DarkE', 'usertype1'),
('DeepOre', 'usertype1'),
('DeepSpace', 'usertype1'),
('DrillX', 'usertype1'),
('Exxon', 'usertype1'),
('FBI', 'usertype1'),
('Google', 'usertype1'),
('HannaH', 'usertype1'),
('HeliumIndustries', 'usertype1'),
('NASA', 'usertype1'),
('SpaceGem', 'usertype1'),
('Spacetronics', 'usertype1'),
('SpaceX', 'usertype1'),
('WideGalaxy', 'usertype1'),
('Xfinity', 'usertype1');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE IF NOT EXISTS `services` (
  `usertype` varchar(65) NOT NULL,
  `service` varchar(767) NOT NULL,
  PRIMARY KEY (`usertype`),
  UNIQUE KEY `usertype` (`usertype`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`usertype`, `service`) VALUES
('usertype1', 'accessGranted'),
('usertype2', 'accessDenied');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `username` varchar(65) NOT NULL,
  `pass_word` varchar(767) NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- RELATIONS FOR TABLE `users`:
--   `username`
--       `groups` -> `username`
--

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`username`, `pass_word`) VALUES
('AAGC', '8aeb76155cfdf0ee5fc46655132e4ab2e0948ff31a1e3d59b9c6bda3c64c1e76a59be6fadd6d23c2fa54d3549b6ab0abd87359f903a2a8494005ac4900e10923'),
('Administrator', 'e23b1a1b17de31c73bcfc9e66a35763ebaa863ea1a6535b44da077a11c14396fbab10153029bb65d75950ecb05930dd1207573c620f4eaf2c5ca3a4a5eae0b3a'),
('AlyTech', 'a6bb12a6f9283f8b2513d322efb806267f485d2d811e893a6bd29dd0fae612f682b3151a956d8b50def19f9be07d71382757d530034c642bd4c52854674f44c1'),
('DarkE', '19af7d79a43633d7c92e598955e7202b4ac9ed839a8f354f385267d1889fe305cdaeffa4354585344b5c37a6ca1ebd080d82d3058f7ffb789302144a77f1f2d3'),
('DeepOre', '3e47a77d278ad9444f7ae3eff283b2e1e2ed8ff14c72610e78492ed1a4eb64ae4ec79165db8509ade9d263b8a0a2388f28d33fdd0784a830d66c22ba1b9b16bb'),
('DeepSpace', '343792ca0b731ccbe3534e3b8d2e4327e8ed429350d29238a44d0c585090e0053696ba981ced0cdf43b9fc60473294720e1d0bb077bd999a10973306f546b406'),
('DrillX', 'a99b4793cce911b6c4c1dcd67a4d7b98aee083c820bf9ddcd03515eebfa412f3cb3b553cbe3cd8fc23cb052323a984ea1c0323530313c1f39c317d4992b7eed4'),
('Exxon', '96fa70d5fe134e85d0ebdca1884d04704372a8222f765f5f4e528f2e71c9431ed0f65614e687e27d078baceaf91e67e3fd8f33c9f3c5904c0cb2d618b66bd2bf'),
('FBI', '37cd5f4774117483d2ce962fc24ceb99813719627af36bd00907520dc6fc8dbc281d472ff59691e13ae80f2fb1f27842e7ea5635879d3ece0d29cac97ca80c6d'),
('Google', '3f55989589cbc619beb799b7e17b22b52bf5371a7945624c7498a4612e098627bef7e8e94bb7a01abe25f85154a130ea761b4870900dc19dc64ed3c709a753c0'),
('HannaH', '55a753c0f69ce0de14439452532c1a0b0ddd033cb24541453eaaa2f0a46e85f530b7590cd4ba5ed960b72f1c73b9b18818a45d74c7626bdca5fd9e3e8fababa8'),
('HeliumIndustries', 'a707d4fe840849e8a61f371904fd0366a3041fd5ed42b44ffdf51d719593c779440bb831d48cc850fe9c240e65b3116cf1d7234e6d7601c9d77141fda2ba213d'),
('NASA', '0c51df2b2c822298f385641d761ecbe65e328359d49584e06da3f89a00c6cc2a26f8fe0b6bdc7ed7625e66ec108532d562a79c2153acf6a8bbba73dacd26790e'),
('SpaceGem', 'c1539a259b74f1d71244fd777bf1482e5ad83ffdb9614580ed3b96f9822024c599c35f7802013e612f3b6dfa63d050e626c1dcdf65c046119dd8453b128f7136'),
('Spacetronics', '58b533e9978207e01b541b344f02426841b1c32048beb04fa276da29fc939367f3f5778b15a433039d6761e7115ebae8f6c303196c20a658ffce8b3ecb64a639'),
('SpaceX', '09c3374377c17f964b6c3732b2a0c88faf1525134ffb97675e73b01d91da7c1fdaac06901ef5b6a8c888dad43fa94583c32f0f86815d45385e7aa01cb27a41fb'),
('WideGalaxy', 'd5e93bf51fe54ddab6800a407d1408e4c9f1a886b556d9e472837c542d45f57e113e93e76103453b3433f38cc425cd1e10388fce126aac5da46f1621f1f875be'),
('Xfinity', '9d36e073839cf81999121decd5e9b5ccc5748afe00eca60121226d55a62f72b47a15337aab8ac901143051509130bad82a8cf2269f99d55e127e8bad39d8fc70');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`username`) REFERENCES `groups` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;
SET FOREIGN_KEY_CHECKS=1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
