/*
This file contains sql queries to create all the tables or views used in this project
*/

/*Table to store film information*/
CREATE TABLE IF NOT EXISTS W2W_Films (
    film_key text
	,title text
    ,year int
    ,description text
    ,platform text
    ,tag text
	,timestamp_film TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	,PRIMARY KEY (film_key(32)) );

/*Table to store user information*/
CREATE TABLE IF NOT EXISTS W2W_Users (
    user_key text
	,user_name text
	,timestamp_u TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	,PRIMARY KEY (user_key(32)) );
	
/*Table to store group information*/
CREATE TABLE IF NOT EXISTS W2W_Groups (
    group_key text
	,group_name text
	,timestamp_g TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	,PRIMARY KEY (group_key(32)) );

/*Table to store group user mapping*/
CREATE TABLE IF NOT EXISTS W2W_Group_User_Mapping (
    group_key text
	,user_key text
	,timestamp_gu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	,PRIMARY KEY (group_key(32), user_key(32)) );

/*Table to store user film ratings*/
CREATE TABLE IF NOT EXISTS W2W_User_Rating (
    user_key text
	,film_key text
	,rating int
	,timestamp_ur TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	,PRIMARY KEY (user_key(32), film_key(32)) );
	
	
	