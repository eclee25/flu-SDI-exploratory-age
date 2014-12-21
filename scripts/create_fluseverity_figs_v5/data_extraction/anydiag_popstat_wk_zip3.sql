/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 10/31/14
Function: extract SDI data any diagnosis visits for total population to adjust spatial data by coverage
- any diagnosis visits by zip3 by week
- include only outpatient facility and office/OP clinics data

Command Line: mysql < anydiag_popstat_wk_zip3.sql | sed 's/\t/,/g' > /home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/anydiag_allweeks_outpatient_zip3.csv
Data: flu table: SDI
*/

SELECT season.SEASON_NUM, flu.WEEK, flu.PATIENT_ZIP3, sum(flu.ANY_DIAG_VISIT_CT)
from flu right join season on (flu.week = season.week)
where (flu.SERVICE_PLACE = "OFFICE/OP CLINICS" or flu.SERVICE_PLACE = "OUTPATIENT FACILITY") and flu.PATIENT_ZIP3 <> "TOT" and flu.AGEGROUP = "TOTAL"
group by season.SEASON_NUM, flu.WEEK, flu.PATIENT_ZIP3
;




