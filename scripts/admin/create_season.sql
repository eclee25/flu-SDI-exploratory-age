/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 4/17/13
Function: Create table that lists week, week of year and season number; week 40 from year 1 to week 20 in year 2 == 1 season

Command Line: run in parts
Data: flu table: SDI
*/

-- this code needs to be run in two separate parts; first data needs to be exported. once exported, a new column will be added manually that represents the season number. the expanded table will be imported into mysql as a new table called "season"

-- export data 
select distinct week, weekofyear(week) from flu order by week
INTO OUTFILE '/tmp/season2.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

-- season number column was added using libreoffice calc

-- import new table as season. comment out export data and run as script with command 
-- mysql --local-infile -u elizabeth -pbansa11ab <create_season.sql

USE sdi;
DROP TABLE if exists season;

CREATE TABLE season (
	WEEK DATE,
	WK_NUM INT(2),	
	SEASON_NUM INT(2),
	SMALL_SEAS_NUM INT(2)
);	
	
LOAD DATA LOCAL INFILE '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_import/season2.csv' INTO TABLE season
FIELDS TERMINATED BY ','
(WEEK, WK_NUM, SEASON_NUM, SMALL_SEAS_NUM)
;


