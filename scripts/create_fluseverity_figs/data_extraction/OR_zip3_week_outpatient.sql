/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 4/29/14
Function: Export data to calculate OR by HHS region
Adapted from OR_zip3_week.sql

Command Line: mysql -u elizabeth -pbansa11ab mysqltemplate.sql
Data: flu table: SDI
*/

SELECT season.SEASON_NUM, flu.WEEK, flu.patient_zip3, child.MARKER, sum(flu.ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE (flu.SERVICE_PLACE = "OFFICE/OP CLINICS" or flu.SERVICE_PLACE = "OUTPATIENT FACILITY") and flu.patient_zip3 <> 'TOT'
GROUP BY season.SEASON_NUM, flu.WEEK, flu.patient_zip3, child.MARKER
INTO OUTFILE '/tmp/OR_zip3_week_outpatient2.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;


SELECT season.SEASON_NUM, flu.patient_zip3, flu.AGEGROUP, flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.popstat <> 0 and child.MARKER <> 'O' and flu.patient_zip3 <> 'TOT'
GROUP BY season.SEASON_NUM, flu.patient_zip3, flu.AGEGROUP
INTO OUTFILE '/tmp/popstat_zip3_season.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

--- check why certain zip3s were in OR dataset but not popstat dataset
SELECT season.SEASON_NUM, flu.WEEK, flu.patient_zip3, flu.AGEGROUP, child.MARKER, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE (flu.SERVICE_PLACE = "OFFICE/OP CLINICS" or flu.SERVICE_PLACE = "OUTPATIENT FACILITY") and child.MARKER <> 'O' and flu.patient_zip3 = '753' and season.SEASON_NUM = 2
GROUP BY season.SEASON_NUM, flu.WEEK, flu.patient_zip3, child.MARKER, flu.AGEGROUP
;
