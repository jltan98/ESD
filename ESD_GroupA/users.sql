-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Feb 27, 2021 at 02:35 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `users` 
--
CREATE DATABASE IF NOT EXISTS `users` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `users`;

-- --------------------------------------------------------


--
-- Table structure for table `investmentCounsellor`
--

DROP TABLE IF EXISTS `investmentCounsellor`;
CREATE TABLE IF NOT EXISTS `investmentCounsellor` (
  `IC_id` int(11) NOT NULL AUTO_INCREMENT,
  `IC_name` varchar(64) NOT NULL,
  `IC_chatid` int(32) NOT NULL,
  `IC_accountname` varchar(64) NOT NULL,
  `IC_password` varchar(64) NOT NULL,
  PRIMARY KEY (`IC_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `investmentCounsellor`
--

INSERT INTO `investmentCounsellor` (`IC_id`, `IC_name`, `IC_chatid`, `IC_accountname`, `IC_password` ) VALUES
(1, 'John James', '747290992', 'JohnJames', SHA1('johnjames123')),
(2, 'Stella Ross', '747290992', 'StellaRoss', SHA1('stellaross234')),
(3, 'Natalie Vande', '747290992', 'NatalieVande', SHA1('natalievande345')),
(4, 'Thomas Addins', '747290992', 'ThomasAddins', SHA1('thomasaddins456'));

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
CREATE TABLE IF NOT EXISTS `client` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_name` varchar(64) NOT NULL,
  `client_password` varchar(64) NOT NULL,
  `client_age` int(3) NOT NULL,
  `client_chatid` int(32) NOT NULL,
  `created_date` date NOT NULL,
  `client_type` varchar(64) NOT NULL,
  `client_accountname` varchar(64) NOT NULL,
  `investment_id` varchar(1064) NOT NULL,
  `ticker_name` varchar (64) NOT NULL,
  `stock_name` varchar (1064) NOT NULL,
  `IC_id` int(11) NOT NULL,

  PRIMARY KEY (`client_id`),
  KEY `FK_IC_id` (`IC_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `client`
--

INSERT INTO `client` (`client_id`, `client_name`, `client_password`, `client_age`, `client_chatid`, `created_date`, `client_type`, `client_accountname`, `investment_id`,`ticker_name`, `stock_name`, `IC_id`) VALUES
(1, 'Jane Austen', SHA1('jane_01'), 56, '174986050',  '2021-03-27', 'risk seeker', 'JaneAusten', '510015, 510014', 'JAZZ, AAPL', 'Jazz Pharmaceuticals, Apple', 1),
(2, 'Austin Jenkins', SHA1('austin_02'), 35, '438288068', '2021-03-28', 'risk adverse', 'AustinsJenkins', '410008, 410011', 'BABA, BA', 'Alibaba Group, Boeing', 2),
(3, 'Randell Lenn', SHA1('randell_03'), 40, '762028540', '2021-03-28', 'risk neutral', 'RandellLenn', '310005, 310016', 'BGCP, CATY', 'BGC Partners, Cathay General Bancorp', 3),
(4, 'Anna Lee', SHA1('anna_04'), 30, '219144899','2021-03-28', 'risk adverse', 'AnnaLee', '410001, 401003', 'IBM, K', 'International Business Machines, Kellogg', 4);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `client`
--
ALTER TABLE `client`
  ADD CONSTRAINT `FK_IC_id` FOREIGN KEY (`IC_id`) REFERENCES `investmentCounsellor` (`IC_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;
-- 

--
-- Constraints for dumped tables
--

--
-- Constraints for table `investmentCounsellor`
--
-- ALTER TABLE `investmentCounsellor`
--   ADD CONSTRAINT `FK_client_id` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON DELETE CASCADE ON UPDATE CASCADE;
-- COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
