CREATE DATABASE IF NOT EXISTS `ArtWork`; 

USE `ArtWork`;

CREATE TABLE `Users` (
    `username` varchar(40),
    `email` varchar(40), 
    `password` varchar(40)
);

CREATE TABLE `Posts`(
    `title` varchar(50),
    `description` varchar(300),
    `price` varchar(10),
    `imageurl` varchar(2048)
    
);