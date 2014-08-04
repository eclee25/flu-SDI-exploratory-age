/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 4/27/14
Function: extract SDI data that will be used to make supplemental figure of zOR metric vs. acute to non-acute ILI cases
- acute ILI cases by week: service_place = 'INPATIENT ACUTE CARE FACILITY' or 'EMERGENCY ROOM/URGENT CARE FAC'
- F1.csv --> non-acute ILI cases by week: service_place = 'OFFICE/OP CLINICS' or 'OUTPATIENT FACILITY'
- popstat by year


Command Line: mysql -u elizabeth -pbansa11ab sdi ILI_popstat_anydiag_wk.sql
Data: flu table: SDI
*/

SELECT season.SEASON_NUM, flu.WEEK, year(flu.WEEK), week(flu.WEEK), sum(flu.ILI_m), sum(ANY_DIAG_VISIT_CT), flu.popstat
from flu right join season on (flu.week = season.week)
where (flu.SERVICE_PLACE = "INPATIENT ACUTE CARE FACILITY" or flu.SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC") and flu.PATIENT_ZIP3 = "TOT" and flu.AGEGROUP = "TOTAL"
group by season.SEASON_NUM, flu.WEEK
INTO OUTFILE '/tmp/Supp_acuteILI_wk.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

/* 8/4/14 - added for reference to F1.csv fields. Data used for Supp_zOR_CFR_CHR.py plot (zOR vs. inpatient/outpatient ILI)
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



