/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: July 1, 2013
Function: Explore and export data to draw US level choropleths and maps of ILI incidence by popstat

# edits 7/18/13
1) export data by season, zip3, ILI, popstat for incidence by season movie map

Command Line: mysql -u elizabeth -pbansa11ab mysqltemplate.sql
Data: flu table: SDI
*/


-- export data by week, zip3, ILI, popstat value

SELECT season.SEASON_NUM, flu.WEEK, flu.patient_zip3, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.AGEGROUP = "TOTAL"
GROUP BY season.SEASON_NUM, flu.WEEK, flu.patient_zip3
INTO OUTFILE '/tmp/choropleth_v7-1-13.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
-- sum ILI_m not needed

-- check
SELECT season.SEASON_NUM, flu.WEEK, flu.patient_zip3, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.AGEGROUP = "TOTAL" and flu.WEEK = '2009-10-04' and flu.patient_zip3 = '999'
GROUP BY season.SEASON_NUM, flu.WEEK, flu.patient_zip3;

SELECT season.SEASON_NUM, flu.WEEK, flu.patient_zip3, flu.ILI_m, flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.AGEGROUP = "TOTAL" and flu.WEEK = '2009-10-04' and flu.patient_zip3 = '999'
GROUP BY season.SEASON_NUM, flu.WEEK, flu.patient_zip3;

-- check
SELECT season.SEASON_NUM, flu.WEEK, flu.patient_zip3, flu.AGEGROUP, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.WEEK = '2009-10-04' and flu.patient_zip3 = '999'
GROUP BY season.SEASON_NUM, flu.WEEK, flu.patient_zip3, flu.AGEGROUP;

SELECT season.SEASON_NUM, flu.WEEK, flu.patient_zip3, flu.AGEGROUP, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE <> "TOTAL" and flu.WEEK = '2009-10-04' and flu.patient_zip3 = '999'
GROUP BY season.SEASON_NUM, flu.WEEK, flu.patient_zip3, flu.AGEGROUP;

SELECT flu.WEEK, flu.patient_zip3, flu.AGEGROUP, flu.SERVICE_PLACE, flu.ILI_m, flu.popstat
from flu
WHERE flu.WEEK = '2009-10-04' and flu.patient_zip3 = '999'
GROUP BY flu.patient_zip3, flu.AGEGROUP;

-- export data by season, zip3, ILI, popstat value
SELECT season.SEASON_NUM, flu.patient_zip3, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.AGEGROUP = "TOTAL" and (month(flu.WEEK) > 9 or month(flu.WEEK) <4) and flu.patient_zip3 <> "TOT"
GROUP BY season.SEASON_NUM, flu.patient_zip3
INTO OUTFILE '/tmp/choropleth_seasonincid_v7-1-13.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
; 
-- exported July 19, 2013

-- check
SELECT season.SEASON_NUM, flu.WEEK, flu.patient_zip3, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.AGEGROUP = "TOTAL" and season.SEASON_NUM = 10 and (month(flu.WEEK) > 9 or month(flu.WEEK) <4) and flu.patient_zip3 = '982'
GROUP BY season.SEASON_NUM, flu.WEEK
;

















