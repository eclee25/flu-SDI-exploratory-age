/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 10/15/14
Function: extract SDI data to normalize age-specific incidence curves by any diagnosis visits
- any diagnosis visits by week
- include only outpatient facility and office/OP clinics data

Command Line: mysql < anydiag_popstat_wk_age.sql | sed 's/\t/,/g' > /home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/anydiag_allweeks_outpatient_age.csv
Data: flu table: SDI
*/

SELECT season.SEASON_NUM, flu.WEEK, child.MARKER, sum(flu.ANY_DIAG_VISIT_CT)
from flu right join season on (flu.week = season.week) right join child on (child.AGEGROUP = flu.AGEGROUP)
where (flu.SERVICE_PLACE = "OFFICE/OP CLINICS" or flu.SERVICE_PLACE = "OUTPATIENT FACILITY") and flu.PATIENT_ZIP3 = "TOT" 
group by season.SEASON_NUM, flu.WEEK, child.MARKER
;




