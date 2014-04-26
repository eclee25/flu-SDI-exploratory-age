/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 4/26/14
Function: extract SDI data that will be used to make a 10-year chart of ILI % of any diagnosis visits for all age groups/locations by week
- ILI cases by week
- any diagnosis visits by week
- popstat by year
- include only outpatient facility and office/OP clinics data

Command Line: mysql -u elizabeth -pbansa11ab sdi ILI_popstat_anydiag_wk.sql
Data: flu table: SDI
*/

SELECT season.SEASON_NUM, flu.WEEK, year(flu.WEEK), week(flu.WEEK), sum(flu.ILI_m), sum(ANY_DIAG_VISIT_CT), flu.popstat
from flu right join season on (flu.week = season.week)
where (flu.SERVICE_PLACE = "OFFICE/OP CLINICS" or flu.SERVICE_PLACE = "OUTPATIENT FACILITY") and flu.PATIENT_ZIP3 = "TOT" and flu.AGEGROUP = "TOTAL"
group by season.SEASON_NUM, flu.WEEK
INTO OUTFILE '/tmp/F1.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;





