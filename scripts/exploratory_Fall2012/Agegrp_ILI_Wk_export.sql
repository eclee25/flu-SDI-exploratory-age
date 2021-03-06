/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 9/20/12
Function: Export SDI flu data - ILI counts, total visit counts, and ILI proportion by week by age group

Command Line: mysql -u elizabeth -pBans1Lab! <Agegrp_ILI_Wk_export.sql
*/
USE sdi;

SELECT AGEGROUP, WEEK, ILI_m, ANY_DIAG_VISIT_CT, ILI_m/ANY_DIAG_VISIT_CT as ILI_prop FROM flu
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3 = "TOT" 
GROUP BY AGEGROUP, WEEK
INTO OUTFILE '/tmp/Agegrp_ILI_Wk.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

/*note that 2000 data is only the last week of December and 2010 data exists only through the end of June*/

/*check that weekly ILI counts sum to yearly ILI counts

SELECT AGEGROUP, WEEK, ILI_m, ANY_DIAG_VISIT_CT, ILI_m/ANY_DIAG_VISIT_CT as ILI_prop FROM flu
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3 = "TOT" AND (AGEGROUP = "2-4 YEARS" OR AGEGROUP = "60-69 YEARS")
GROUP BY AGEGROUP, WEEK
INTO OUTFILE '/tmp/ILIct_check.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT AGEGROUP, YEAR(WEEK), sum(ILI_m), sum(ANY_DIAG_VISIT_CT) FROM flu
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3 = "TOT" AND (AGEGROUP = "2-4 YEARS" OR AGEGROUP = "60-69 YEARS")
GROUP BY AGEGROUP, YEAR(WEEK)
; /*week sums match year sums*/

/*check that weekly ILI counts sum to TOTAL ILI counts for all age groups
SELECT WEEK, sum(ILI_m), sum(ANY_DIAG_VISIT_CT) FROM flu
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3 = "TOT" AND AGEGROUP != "TOTAL"
GROUP BY WEEK
INTO OUTFILE '/tmp/ILIcttot_check2.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

SELECT AGEGROUP, WEEK, ILI_m, ANY_DIAG_VISIT_CT FROM flu
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3 = "TOT" AND AGEGROUP = "TOTAL"
GROUP BY WEEK
; /*weekly agegroup sums match total agegroup column for ILI_m and ANY_DIAG_VISIT_CT



