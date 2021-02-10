/*
This file contains sql queries to create all the tables or views used in this project
*/

/*Table to store film information*/
CREATE TABLE IF NOT EXISTS W2W_Films (
    title text
    ,year int
    ,description text
    ,platform text
    ,tag text
	,timestamp_film TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	,PRIMARY KEY (title(50), year) );

/*Table to store user information*/
CREATE TABLE IF NOT EXISTS W2W_Users (
    user_name text
	,timestamp_u TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	,PRIMARY KEY (user_name(50)) );
	
/*Table to store group information*/
CREATE TABLE IF NOT EXISTS W2W_Groups (
    group_name text
	,timestamp_g TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	,PRIMARY KEY (group_name(50)) );

/*Table to store group user mapping*/
CREATE TABLE IF NOT EXISTS W2W_Group_User_Mapping (
    group_name text
	,user_name text
	,timestamp_gu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	,PRIMARY KEY (group_name(50), user_name(50)) );

