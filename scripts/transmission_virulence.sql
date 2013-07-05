/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 3/27/13
Function: Export SDI flu data into different shapes to draw general plots

Command Line: mysql -u elizabeth -pbansa11ab  (run in chunks)
Data: flu table: SDI
stdpop table: http://seer.cancer.gov/stdpopulations/stdpop.singleages.html
*/

use sdi;

SELECT WEEK, sum(ILI_m), sum(ANY_DIAG_VISIT_CT), sum(ILI_m)/sum(ANY_DIAG_VISIT_CT)*100 as ILI_incid_perc from flu
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND AGEGROUP = "TOTAL"
GROUP BY WEEK
INTO OUTFILE '/tmp/H1a.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

SELECT WEEK, sum(ILI_m), sum(ANY_DIAG_VISIT_CT) from flu
WHERE SERVICE_PLACE = "INPATIENT ACUTE CARE FACILITY" AND PATIENT_ZIP3= "TOT" AND AGEGROUP = "TOTAL"
GROUP BY WEEK
INTO OUTFILE '/tmp/H1b.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
