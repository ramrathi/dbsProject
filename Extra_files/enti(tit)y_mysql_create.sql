CREATE DATABASE dbsproject;

USE dbsproject;

CREATE TABLE `Users` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`name` varchar(255) NOT NULL,
	`password` varchar(255) NOT NULL,
	`dob` DATE NOT NULL,
	`gender` INT(1) NOT NULL,
	`bio` VARCHAR(255),
	`city` varchar(255),
	`country` varchar(255),
	`email` varchar(50) UNIQUE,
	`phone_number` varchar(15) UNIQUE,
	`wallet` INT(10) NOT NULL UNIQUE DEFAULT '50',
	PRIMARY KEY (`id`)
);

CREATE TABLE `Posts` (
	`p_id` INT(10) NOT NULL AUTO_INCREMENT,
	`u_id` INT(10) NOT NULL,
	`content` varchar(500) NOT NULL,
	`time_stamp` TIMESTAMP NOT NULL,
	`photo` blob(1000),
	`location` varchar(50),
	`community` INT(10),
	PRIMARY KEY (`p_id`)
);

CREATE TABLE `Messages` (
	`m_id` INT(10) NOT NULL AUTO_INCREMENT,
	`From` INT(10) NOT NULL,
	`To` INT(10) NOT NULL,
	`Content` varchar(500) NOT NULL,
	`media` blob(500),
	`timestamp` TIMESTAMP,
	PRIMARY KEY (`m_id`)
);

CREATE TABLE `Events` (
	`e_id` INT(10) NOT NULL AUTO_INCREMENT,
	`host` INT(10) NOT NULL,
	`location` varchar(50) NOT NULL,
	`description` varchar(255),
	`media` blob(255),
	PRIMARY KEY (`e_id`)
);

CREATE TABLE `Community` (
	`c_id` INT(10) NOT NULL AUTO_INCREMENT,
	`name` varchar(50) NOT NULL,
	`description` varchar(255),
	PRIMARY KEY (`c_id`)
);

CREATE TABLE `Market` (
	`i_id` INT(10) NOT NULL AUTO_INCREMENT,
	`title` varchar(50) NOT NULL,
	`description` varchar(255),
	`price` INT(10),
	`seller` INT(10) NOT NULL,
	`sold` INT(1) NOT NULL,
	PRIMARY KEY (`i_id`)
);

CREATE TABLE `Music` (
	`s_id` INT(10) NOT NULL AUTO_INCREMENT,
	`name` varchar(50) NOT NULL,
	`artist` varchar(50) NOT NULL,
	`album` varchar(50),
	`year` INT(10),
	`price` INT(10) NOT NULL,
	PRIMARY KEY (`s_id`)
);

CREATE TABLE `Transactions` (
	`t_id` INT(10) NOT NULL AUTO_INCREMENT,
	`from` INT(10) NOT NULL,
	`to` INT(10) NOT NULL,
	`money` INT(10) NOT NULL,
	`timestamp` TIMESTAMP NOT NULL,
	`message` varchar(255),
	PRIMARY KEY (`t_id`)
);

CREATE TABLE `Friends` (
	`u1_id` INT(10) NOT NULL,
	`u2_id` INT(10) NOT NULL,
	PRIMARY KEY (`u1_id`,`u2_id`)
);

CREATE TABLE `Comments` (
	`comm_id` INT(10) NOT NULL AUTO_INCREMENT,
	`post_id` INT(10) NOT NULL,
	`user_id` INT(10) NOT NULL,
	`content` varchar(255) NOT NULL,
	`timestamp` TIMESTAMP NOT NULL,
	PRIMARY KEY (`comm_id`)
);

CREATE TABLE `Playlist` (
	`user_id` INT(10) NOT NULL,
	`song_id` INT(10) NOT NULL,
	PRIMARY KEY (`user_id`,`song_id`)
);

CREATE TABLE `Attending` (
	`event_id` INT(10) NOT NULL,
	`user_id` INT(10) NOT NULL,
	PRIMARY KEY (`event_id`,`user_id`)
);

CREATE TABLE `Belongs` (
	`user_id` INT(10) NOT NULL,
	`community_id` INT(10) NOT NULL,
	PRIMARY KEY (`user_id`,`community_id`)
);

CREATE TABLE `Payment` (
	`user_id` INT(10) NOT NULL,
	`item_id` INT(10) NOT NULL,
	PRIMARY KEY (`user_id`,`item_id`)
);

ALTER TABLE `Posts` ADD CONSTRAINT `Posts_fk0` FOREIGN KEY (`u_id`) REFERENCES `Users`(`id`);

ALTER TABLE `Posts` ADD CONSTRAINT `Posts_fk1` FOREIGN KEY (`community`) REFERENCES `Community`(`c_id`);

ALTER TABLE `Messages` ADD CONSTRAINT `Messages_fk0` FOREIGN KEY (`From`) REFERENCES `Users`(`id`);

ALTER TABLE `Messages` ADD CONSTRAINT `Messages_fk1` FOREIGN KEY (`To`) REFERENCES `Users`(`id`);

ALTER TABLE `Events` ADD CONSTRAINT `Events_fk0` FOREIGN KEY (`host`) REFERENCES `Users`(`id`);

ALTER TABLE `Market` ADD CONSTRAINT `Market_fk0` FOREIGN KEY (`seller`) REFERENCES `Users`(`id`);

ALTER TABLE `Transactions` ADD CONSTRAINT `Transactions_fk0` FOREIGN KEY (`from`) REFERENCES `Users`(`id`);

ALTER TABLE `Transactions` ADD CONSTRAINT `Transactions_fk1` FOREIGN KEY (`to`) REFERENCES `Users`(`id`);

ALTER TABLE `Friends` ADD CONSTRAINT `Friends_fk0` FOREIGN KEY (`u1_id`) REFERENCES `Users`(`id`);

ALTER TABLE `Friends` ADD CONSTRAINT `Friends_fk1` FOREIGN KEY (`u2_id`) REFERENCES `Users`(`id`);

ALTER TABLE `Comments` ADD CONSTRAINT `Comments_fk0` FOREIGN KEY (`post_id`) REFERENCES `Posts`(`p_id`);

ALTER TABLE `Comments` ADD CONSTRAINT `Comments_fk1` FOREIGN KEY (`user_id`) REFERENCES `Users`(`id`);

ALTER TABLE `Playlist` ADD CONSTRAINT `Playlist_fk0` FOREIGN KEY (`user_id`) REFERENCES `Users`(`id`);

ALTER TABLE `Playlist` ADD CONSTRAINT `Playlist_fk1` FOREIGN KEY (`song_id`) REFERENCES `Music`(`s_id`);

ALTER TABLE `Attending` ADD CONSTRAINT `Attending_fk0` FOREIGN KEY (`event_id`) REFERENCES `Events`(`e_id`);

ALTER TABLE `Attending` ADD CONSTRAINT `Attending_fk1` FOREIGN KEY (`user_id`) REFERENCES `Users`(`id`);

ALTER TABLE `Belongs` ADD CONSTRAINT `Belongs_fk0` FOREIGN KEY (`user_id`) REFERENCES `Users`(`id`);

ALTER TABLE `Belongs` ADD CONSTRAINT `Belongs_fk1` FOREIGN KEY (`community_id`) REFERENCES `Community`(`c_id`);

ALTER TABLE `Payment` ADD CONSTRAINT `Payment_fk0` FOREIGN KEY (`user_id`) REFERENCES `Users`(`id`);

ALTER TABLE `Payment` ADD CONSTRAINT `Payment_fk1` FOREIGN KEY (`item_id`) REFERENCES `Market`(`i_id`);
