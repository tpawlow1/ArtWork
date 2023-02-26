CREATE DATABASE IF NOT EXISTS `ArtWork`; 

USE `ArtWork`;

CREATE TABLE `Users` (
    `username` varchar(40),
    `email` varchar(40), 
    `password` varchar(40),
    'bio' varchar(255)
);