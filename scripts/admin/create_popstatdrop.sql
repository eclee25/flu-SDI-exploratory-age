/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 5/16/13
Function: Create a table that lists the zipcode prefixes that will be completely dropped from our analysis due to missing popstat data. These data have very small ILI counts as well.

Command Line: mysql --local-infile -u elizabeth -pbansa11ab <create_popstatdrop.sql
Data: flu table: SDI
*/

----- PROLOGUE from OR_zipcode_v5-16-13.sql -----
-- identify zipcodes that will be included --
select distinct patient_zip3, popstat from flu where popstat = ' ';
-- there were 52 zipcodes that had missing values for at least one row in popstat 
-- compare this list of 52 to http://en.wikipedia.org/wiki/List_of_ZIP_code_prefixes locations. Many zipcodes belong to the IRS, government, military, or US territories, or are otherwise not in use in a normal way
-- of these 52 zipcodes, the following should be explored further because they appear to be normal zipcodes that should have valid data (311, 332, 398, 509, 555, 753, 772, 851, 872, 885, 889, 901, 942)
-- 311, 332, 509, 555, 753, 772, 872, 885, 889, 901, 942: all missing popstat
-- 398: missing 2002 popstat but not in other years
-- 851: missing popstat across multiple months in multiple years but none are missing in 2010
-- SO-- of the 52 zipcode prefixes that have any missing popstat values, include 398 and 851 only
select patient_zip3, week, agegroup, sum(ILI_m), popstat from flu where (patient_zip3 = 311) and popstat <> ' ' 
group by patient_zip3, week, agegroup
;
-- create a table that is a list of zipcode prefixes that will be completely dropped from our analysis (See create_popstatdrop.sql in /Dropbox/Elizabeth_Bansal_Lab/SDI_Data/scripts/admin

select distinct patient_zip3 from flu 
where popstat = ' '
INTO OUTFILE '/tmp/popstatdrop2.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
-- edit exported data in medit to remove 398 and 851

--------------------------------------------------

--import new table as popstatdrop. cut out all above and run as script with command: mysql --local-infile -u elizabeth -pbansa11ab <create_popstatdrop.sql

USE sdi;
DROP TABLE if exists popstatdrop;

CREATE TABLE popstatdrop (
	ZIP3 VARCHAR(3)
);	
LOAD DATA LOCAL INFILE '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_import/popstatdrop2.csv' INTO TABLE popstatdrop
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
(ZIP3)
;



