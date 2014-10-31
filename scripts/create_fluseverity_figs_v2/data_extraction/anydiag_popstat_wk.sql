/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 10/11/14
Function: extract SDI data that will be used to make an any diagnosis visit / population size per 100,000 time series chart
- any diagnosis visits by week
- include only outpatient facility and office/OP clinics data

Command Line: mysql < anydiag_popstat_wk.sql | sed 's/\t/,/g' > anydiag_outpatient_allweeks.csv
Data: flu table: SDI
*/

SELECT season.SEASON_NUM, flu.WEEK, flu.ANY_DIAG_VISIT_CT, flu.popstat
from flu right join season on (flu.week = season.week)
where (flu.SERVICE_PLACE = "OFFICE/OP CLINICS" or flu.SERVICE_PLACE = "OUTPATIENT FACILITY") and flu.PATIENT_ZIP3 = "TOT" and flu.AGEGROUP = "TOTAL"
group by season.SEASON_NUM, flu.WEEK
;





