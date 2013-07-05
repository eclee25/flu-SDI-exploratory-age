/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 5/17/13
Function: Create a table with year, zip3, childmarker, sum(popstat) to use as a reference for age-specific population within a zipcode prefix. First an intermediate table needs to be made because summing popstat with reference to the childmarker will not be done correctly if done in a single summing step because the data is separated in weeks and the reference table should be in years.

known issues with the psref table:
- some zipcodes did not have entries for each age group every year, which means that summing the popstats across agegroups for each year will not yield the entire population size. this is problematic when trying to use these sums for the denominators 
- the popstat sums will be more accurate for more populous zipcodes than less populous zipcodes because there is a greater likelihood of having a complete dataset.
- total population size for all age groups for a single zipcodes each year seems accurate, however.

Command Line: 
(to create new mysql table) mysql --local-infile -u elizabeth -pbansa11ab <create_psref.sql
(run select statements within mysql, not as script)
Data: flu table: SDI
*/

/*-- create an intermediate table that will allow you to generate the final table*/

/*
USE sdi;

select year(flu.week) as year, pskeep.zip3, child.marker, flu.agegroup, flu.popstat from flu right join pskeep on (pskeep.zip3 = flu.patient_zip3) right join child on (child.agegroup = flu.agegroup)
where flu.service_place = "TOTAL"
group by year(flu.week), pskeep.zip3, child.marker, flu.agegroup
INTO OUTFILE '/tmp/psref_int.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
*/

/* load intermediate table into mysql */
/*
USE sdi;
DROP TABLE if exists psref_int;

CREATE TABLE psref_int (
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	YEAR YEAR(4),
	ZIP3 VARCHAR(3),
	MARKER VARCHAR(2),
	AGEGROUP VARCHAR(12),
	POPSTAT INT
	
);	
LOAD DATA LOCAL INFILE '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_import/psref_int.csv' INTO TABLE psref_int
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
(YEAR, ZIP3, MARKER, AGEGROUP, POPSTAT)
;
*/

/* check final data pull from intermediate table and create a new table in mysql from this data pull */
/*
select year, zip3, marker, sum(popstat) from psref_int
group by year, zip3, marker
;
*/

/* perform checks comparing psref_int to sums from the above select statement (checks out) */
/*
select year, zip3, marker, agegroup, popstat from psref_int
where year = 2003 and zip3 = "841"
group by year, zip3, marker, agegroup
;
select year, zip3, marker, sum(popstat) from psref_int
where year = 2003 and zip3 = "841" 
group by year, zip3, marker
;
*/

/* export data to csv file and reimport as mysql table*/
/*
select year, zip3, marker, sum(popstat) from psref_int
group by year, zip3, marker
INTO OUTFILE '/tmp/psref.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
*/

/* reimport data as mysql table */
USE sdi;
DROP TABLE if exists psref;

CREATE TABLE psref (
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	YEAR YEAR(4),
	ZIP3 VARCHAR(3),
	MARKER VARCHAR(2),
	POPSTAT INT
	
);
LOAD DATA LOCAL INFILE '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_import/psref.csv' INTO TABLE psref
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
(YEAR, ZIP3, MARKER, POPSTAT)
;

/* checks on new psref table */ 
select year, zip3, marker, popstat from psref
where zip3 = "200"
group by marker, year
;
select year, zip3, marker, agegroup, popstat from psref_int
where zip3 = "994"
group by year, marker, agegroup
;
select year(week), patient_zip3, popstat from flu
where patient_zip3 = "994" and agegroup = "TOTAL"
group by year(week)
;





