/*
This file contains sql queries to create all the tables or views used in this project
*/

/*Table to store film information*/
CREATE TABLE IF NOT EXISTS W2W_Films (
    film_key int
	,title text
    ,year int
    ,description text
	,duration text
    ,platform text
    ,genres text
	,imdb_rating text
	,netflix_rating text
	,average_rating text
	,the_movie_database_rating text
	,metacritic_rating text
	,rotten_tomatoes_rating text
	,timestamp_film TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	,PRIMARY KEY (film_key) );

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
	,film_key int
	,rating int
	,timestamp_ur TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	,PRIMARY KEY (user_key(32), film_key) );
	
/*Table to store imdb film information - not currently used*/
CREATE TABLE IF NOT EXISTS imdb_films (
    tconst text
	,titleType text
    ,primaryTitle text
    ,originalTitle text
    ,isAdult text
    ,startYear int
	,endYear int
	,runtimeMinutes int
	,genres text
	,averageRating float
	,numVotes int
	,timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	,PRIMARY KEY (tconst(32)) );
	