/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 4/24/14
Function: Grab ILI by age group by season for flu season weeks only

Save in SQL_export/

Command Line: mysql -u elizabeth -pbansa11ab OR_season_outpatient_fluwks.sql
Data: flu table: SDI
*/

-- grab all ILI outpatient cases by age group for each season
SELECT season.SMALL_SEAS_NUM, child.MARKER, sum(flu.ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child on (flu.AGEGROUP = child.AGEGROUP)
WHERE (flu.SERVICE_PLACE = "OFFICE/OP CLINICS" or flu.SERVICE_PLACE = "OUTPATIENT FACILITY") and flu.PATIENT_ZIP3 = "TOT" 
GROUP BY season.SMALL_SEAS_NUM, child.MARKER
INTO OUTFILE '/tmp/OR_season_outpatient_fluwks.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
