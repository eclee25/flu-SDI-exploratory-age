/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 4/24/14
Function: Grab total population by age groups by calendar year

Save in SQL_export/

Command Line: mysql -u elizabeth -pbansa11ab totalpop_age.sql
Data: flu table: SDI
*/

-- grab data for children and adults across weeks for each season
SELECT YEAR(flu.WEEK), flu.AGEGROUP, flu.POPSTAT
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) 
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" 
GROUP BY YEAR(flu.WEEK), flu.AGEGROUP
INTO OUTFILE '/tmp/totalpop_age.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;