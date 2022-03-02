-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 12, 2020 at 02:17 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `recommendation`
--
CREATE DATABASE IF NOT EXISTS `recommendation` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `recommendation`;

-- --------------------------------------------------------

--
-- Table structure for table `recommendation`
--

DROP TABLE IF EXISTS `recommendation`;
CREATE TABLE IF NOT EXISTS `recommendation` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  -- `client_type` varchar(64) NOT NULL,
  -- `client_account` varchar(64) NOT NULL,
  `reco_created_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `investment_id` varchar(64) NOT NULL,
  `ticker_name` varchar (64) NOT NULL,
  `stock_name` varchar (1064) NOT NULL,
  `recommendation` text NOT NULL,
  `comment` text NOT NULL,
  `IC_id` int(11) NOT NULL,
  `IC_chatid` int(32) NOT NULL,
  `status` varchar(64) NOT NULL,

--   `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`client_id`,`investment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping pre-created recommendation data for table `recommendation`
--
INSERT INTO `recommendation` (`client_id`, `reco_created_date`, `recommendation`, `comment`, `investment_id`,`ticker_name`, `stock_name`, `IC_id`,`IC_chatid`, `status`) VALUES
(1, CURRENT_TIMESTAMP,'We recommend shorting Jazz Pharmaceuticals [JAZZ] because at its current share price, it is overvalued by 50 ~70 %, and its price could decline significantly in the next 6~12months or so.', '', '510015', 'JAZZ', 'Jazz Pharmaceuticals', 1,'747290992', ""),
(1, CURRENT_TIMESTAMP,'We recommend longing AAPL [APPLE] because it is undervalued by 20-30%, and its stock price could increase significantly in the next 6-12 months.','', '510014', 'AAPL', 'Apple', 1,'747290992', ""); 
