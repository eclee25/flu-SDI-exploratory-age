/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 9/20/12
Function: Export SDI flu data - ILI counts, total visit counts, and ILI proportion by year by age group

Command Line: mysql -u elizabeth -pBans1Lab! <Agegrp_ILI_Yr_export.sql
*/

USE sdi;

SELECT AGEGROUP, YEAR(WEEK), sum(ILI_m), sum(ANY_DIAG_VISIT_CT), sum(ILI_m)/sum(ANY_DIAG_VISIT_CT) as ILI_prop FROM flu
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3 = "TOT"
GROUP BY AGEGROUP, YEAR(WEEK)
INTO OUTFILE '/tmp/mysql/Agegrp_ILI_Yr.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;


/*note that 2000 data is only the last week of December and 2010 data exists only through the end of June*/

