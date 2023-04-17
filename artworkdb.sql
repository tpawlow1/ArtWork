CREATE DATABASE IF NOT EXISTS `ArtWork`; 

USE `ArtWork`;

CREATE TABLE IF NOT EXISTS `Users` (
    `username` varchar(40) PRIMARY KEY,
    `email` varchar(40), 
    `password` varchar(40),
    `bio` varchar(255),
    `profilePicPath` varchar(2048),
    `isArtist` BOOLEAN DEFAULT false, 
    `Money` DECIMAL(6,2)
);

CREATE TABLE IF NOT EXISTS`Follows`(
    `follower` varchar(255),
    `following` varchar(255),
    PRIMARY KEY (`follower`, `following`)
);

CREATE TABLE IF NOT EXISTS`Posts`(
    `id` varchar(100) PRIMARY KEY,
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
    `tousername` varchar(40), 
    `fromusername` varchar(40), 
    `content` varchar(300), 
    `time` timestamp
);

CREATE TABLE IF NOT EXISTS `Auctions` (
    `auction_id` varchar(100),
    `title` varchar(40), 
    `description` varchar(300),
    `filepath` varchar(2048),
    `user` varchar(40),
    `createdTime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	`endTime` DATETIME NOT NULL,
    `price` DOUBLE,
	`isExpired` BOOLEAN DEFAULT false
);

CREATE TABLE IF NOT EXISTS `Post_Interactions` (	
	`pi_userID` varchar(100),
	`pi_postID` varchar(100),
    `pi_likes` BOOLEAN DEFAULT false,
    `pi_dislikes` BOOLEAN DEFAULT false,
    FOREIGN KEY (`pi_userID`) REFERENCES Users(`username`),
    FOREIGN KEY (`pi_postID`) REFERENCES Posts(`id`)
);
