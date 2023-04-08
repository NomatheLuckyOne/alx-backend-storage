-- Write a script that creates users table 
CREATE TABLE IF NOT EXISTS users (
	id INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL UNIQUE,
	name  Varchar(255),
	PRIMARY KEY (id)
),
