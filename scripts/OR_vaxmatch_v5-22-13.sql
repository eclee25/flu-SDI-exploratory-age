/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 5/22/13	
Function: Pull data needed to create scatterplot of odds ratio vs vaccine strain match for each season.

Command Line: mysql -u elizabeth -pbansa11ab sdi <OR_vaxmatch_v5-22-13.sql;
Data: flu table: SDI

re-exported on 8/7/13 after prominent subtypes were corrected
*/

SELECT * from vaxmatch
INTO OUTFILE '/tmp/vaxmatch2.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;


/* use data exported from odds_c_a_v4-17-13.sql to odds ratio data for each season */


