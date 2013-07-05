/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 5/20/13
Function: Export mysql data to create chart of prominent subtype during flu season by odds ratio of attack rate

Command Line: mysql -u elizabeth -pbansa11ab <OR_subtype_v5-20-13.sql
Data: 
*/
USE sdi;
/* export subtype data */

SELECT * from subtype
INTO OUTFILE '/tmp/subtype3.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

/* use data exported from odds_c_a_v4-17-13.sql to odds ratio data for each season */


