/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 9/2/13
Function: export data for OR by week for all weeks chart

Command Line: mysql -u elizabeth -pbansa11ab mysqltemplate.sql
Data: flu table: SDI
*/



SELECT season.SEASON_NUM, flu.WEEK, child.MARKER, sum(flu.ILI_m) 
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT"
GROUP BY season.SEASON_NUM, flu.WEEK, child.MARKER
INTO OUTFILE '/tmp/OR_allweeks.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

SELECT season.SEASON_NUM, flu.WEEK, child.MARKER, sum(flu.ILI_m) 
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "OFFICE/OP CLINICS" and flu.PATIENT_ZIP3 = "TOT"
GROUP BY season.SEASON_NUM, flu.WEEK, child.MARKER
INTO OUTFILE '/tmp/OR_allweeks_office.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;


SELECT season.SEASON_NUM, flu.WEEK, child.MARKER, sum(flu.ILI_m) 
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE (flu.SERVICE_PLACE = "OFFICE/OP CLINICS" or flu.SERVICE_PLACE = "OUTPATIENT FACILITY") and flu.PATIENT_ZIP3 = "TOT"
GROUP BY season.SEASON_NUM, flu.WEEK, child.MARKER
INTO OUTFILE '/tmp/OR_allweeks_outpatient.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
