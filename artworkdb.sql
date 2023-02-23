CREATE DATABASE IF NOT EXISTS `ArtWork`; 

USE `ArtWork`;

CREATE TABLE IF NOT EXISTS `Users` (
    `username` varchar(40),
    `email` varchar(40), 
    `password` varchar(40)
);

CREATE TABLE IF NOT EXISTS`Posts`(
    `id` varchar(100),
    `title` varchar(50),
    `description` varchar(300),
    `price` numeric(10,2),
    `filepath` varchar(256)
);