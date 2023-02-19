CREATE DATABASE IF NOT EXISTS `ArtWork`; 

USE `ArtWork`;

CREATE TABLE IF NOT EXISTS `Users` (
    `username` varchar(40),
    `email` varchar(40), 
    `password` varchar(40)
);

CREATE TABLE IF NOT EXISTS`Posts`(
    `title` varchar(50),
    `description` varchar(300),
    `price` varchar(10),
    `filepath` varchar(2048)
    
);