/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 5/17/13
Function: Create table pskeep that lists all of the zipcode prefixes that will be kept in our dataset. The select statements to exclude selected data based on their zipcode prefixes (table from popstatdrop

Command Line: mysql --local-infile -u elizabeth -pbansa11ab <create_pskeep.sql
Data: flu table: SDI
*/

--- PROLOGUE ---
SELECT distinct PATIENT_ZIP3 from flu
INTO OUTFILE '/tmp/pskeep2.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

-- does popstat total add up to the values in the dataset or does it include missing data?
select sum(popstat), sum(ILI_m) from flu
where SERVICE_PLACE = "TOTAL" and AGEGROUP = "TOTAL" and PATIENT_ZIP3 <> "TOT" and week = "2010-01-17"
; --sum(popstat), sum(ILI_m) = 308234883, 97045
select popstat, ILI_m from flu
where SERVICE_PLACE = "TOTAL" and AGEGROUP = "TOTAL" and PATIENT_ZIP3 = "TOT" and week = "2010-01-17"
; --popstat ILI_m = 308907497, 97045
--It appears that the total popstat value is larger than the sum of all of the non-zero popstat values so perhaps the total value incorporates some of the missing zipcode prefix data.

-- create a table that is a list of only zipcode prefixes that will be included in our zipcode level analysis (See create_pskeep.sql in /Dropbox/Elizabeth_Bansal_Lab/SDI_Data/scripts/admin/)
-- this seems easier to implement than the popstatdrop analysis
-- edit exported data in medit, not LibreOffice!

--------------------------------------------------

--import new table as pskeep. cut out all above and run as script with command: mysql --local-infile -u elizabeth -pbansa11ab <create_pskeep.sql

-- Question: Does popstat value for the "TOT" zipcode prefix reflect the size of the entire population despite the fact that some popstat data are missing for certain zipcodes?

USE sdi;
DROP TABLE if exists pskeep;

CREATE TABLE pskeep (
	ZIP3 VARCHAR(3)
);	
LOAD DATA LOCAL INFILE '/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_import/pskeep2.csv' INTO TABLE pskeep
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
(ZIP3)
;





