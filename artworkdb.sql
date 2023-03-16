CREATE DATABASE IF NOT EXISTS `ArtWork`; 

USE `ArtWork`;

CREATE TABLE IF NOT EXISTS `Users` (
    `username` varchar(40),
    `email` varchar(40), 
    `password` varchar(40),
    `bio` varchar(255),
    `profilePicPath` varchar(2048)
);

CREATE TABLE IF NOT EXISTS`Posts`(
    `id` varchar(100),
    `title` varchar(50),
    `description` varchar(300),
    `filepath` varchar(2048),
    `user` varchar(40)
);