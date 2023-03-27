CREATE DATABASE IF NOT EXISTS `ArtWork`; 

USE `ArtWork`;

CREATE TABLE IF NOT EXISTS `Users` (
    `username` varchar(40),
    `email` varchar(40), 
    `password` varchar(40),
    `bio` varchar(255),
    `profilePicPath` varchar(2048),
    `isArtist` BOOLEAN DEFAULT false 
);

CREATE TABLE IF NOT EXISTS`Follows`(
    `follower` varchar(255),
    `following` varchar(255),
    PRIMARY KEY ('follower', 'following')
);

CREATE TABLE IF NOT EXISTS`Posts`(
    `id` varchar(100),
    `title` varchar(50),
    `description` varchar(300),
    `filepath` varchar(2048),
    `user` varchar(40),
    `likes` INT,
    `dislikes` INT
);


CREATE TABLE IF NOT EXISTS `Comments`(
    `post_id` varchar(100),
    `comment` varchar(300),
    `user` varchar(40)
);

CREATE TABLE IF NOT EXISTS`Messages`(
    `id` varchar(100),
    `tousername` varchar(40), 
    `fromusername` varchar(40), 
    `content` varchar(300), 
    `time` timestamp

);

