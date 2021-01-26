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




