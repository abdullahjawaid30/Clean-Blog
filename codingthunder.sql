-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 06, 2024 at 02:03 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `codingthunder`
--

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `Sno` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone_number` varchar(50) NOT NULL,
  `msg` text NOT NULL,
  `date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`Sno`, `name`, `email`, `phone_number`, `msg`, `date`) VALUES
(1, 'firstPost', 'firstpost@email.com', '123456789', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.', '2024-09-03 14:59:02'),
(3, 'Hello', 'hello@hello.com', '2323234354', 'hello now', '2024-09-03 15:56:45'),
(4, 'Hello', 'hello@hello.com', '2323234354', 'hello now', '2024-09-03 16:28:54'),
(5, 'Hello', 'hello@hello.com', '2323234354', 'hello now', '2024-09-06 11:36:35');

-- --------------------------------------------------------

--
-- Table structure for table `post`
--

CREATE TABLE `post` (
  `Sno` int(11) NOT NULL,
  `Title` text NOT NULL,
  `tagline` text NOT NULL,
  `slug` varchar(20) NOT NULL,
  `content` text NOT NULL,
  `img_file` varchar(12) NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `post`
--

INSERT INTO `post` (`Sno`, `Title`, `tagline`, `slug`, `content`, `img_file`, `date`) VALUES
(1, 'This is my first post title', 'this is fitrst post', 'first-post', 'This is my first post in Blog website and I am creating this website using FLASK Micro Framework', 'post-bg.jpg', '2024-09-03 17:04:25'),
(2, 'This is Second Post', 'this is second post', 'second-post', 'A Jinja template is simply a text file. Jinja can generate any text-based format (HTML, XML, CSV, LaTeX, etc.). A Jinja template doesn’t need to have a specific extension: .html, .xml, or any other extension is just fine.\r\n\r\nA template contains variables and/or expressions, which get replaced with values when a template is rendered; and tags, which control the logic of the template. The template syntax is heavily inspired by Django and Python.\r\n\r\nBelow is a minimal template that illustrates a few basics using the default Jinja configuration. We will cover the details later in this document:\r\n\r\n', 'home-bg.jpg', '2024-09-06 15:44:55');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`Sno`);

--
-- Indexes for table `post`
--
ALTER TABLE `post`
  ADD PRIMARY KEY (`Sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `Sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `post`
--
ALTER TABLE `post`
  MODIFY `Sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
