/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 7/7/13
Function: 
1) Pull incidence data for only 6 weeks before and after the peak for child and adult populations across all zip3s
2) Pull incidence, zip3, and popstat data for only 6 weeks before and after the peak for child and adult populations
3) Pull incidence for child and adult populations by week for the peak +/- 6 wk span across all zip3s (7/9/13)

Command Line: mysql -u elizabeth -pbansa11ab 
Data: flu table: SDI
*/


/* identify peak weeks for each season */
SELECT season.SMALL_SEAS_NUM, flu.WEEK, flu.ILI_m 
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.patient_zip3 = "TOT" and flu.AGEGROUP = "TOTAL"
GROUP BY flu.WEEK
;

SELECT season.SMALL_SEAS_NUM, flu.WEEK, sum(flu.ILI_m) 
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.patient_zip3 = "TOT" and flu.AGEGROUP = "TOTAL"
GROUP BY flu.WEEK
;

/* the information found above was used to create a new season table, which was updated in create_season.sql. the new field in season is called "SEAS_WK6" */


/* Function 1: incidence data for large populations across all zip3s*/
/* Pull incidence data by season (all zip3s) */
SELECT season.SEAS_WK6, child.MARKER, sum(flu.ILI_m) 
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SEAS_WK6 <> 0
GROUP BY season.SEAS_WK6, child.MARKER
;

/* Old incidence data by season (all zip3s, Oct-May), shown for comparison */
SELECT season.SMALL_SEAS_NUM, child.MARKER, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM <> 0
GROUP BY season.SMALL_SEAS_NUM, child.MARKER
;

/* Function 2: incidence, zip3 and popstat data */
SELECT season.SEAS_WK6, flu.PATIENT_ZIP3, child.MARKER, flu.AGEGROUP, sum(flu.ILI_m), sum(flu.popstat) 
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 <> "TOT" and season.SEAS_WK6 = 2 and child.MARKER <> 'O'
GROUP BY season.SEAS_WK6, flu.PATIENT_ZIP3, flu.AGEGROUP, child.MARKER
;

/* removed sum from popstat */
SELECT season.SEAS_WK6, flu.PATIENT_ZIP3, child.MARKER, flu.AGEGROUP, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 <> "TOT" and season.SEAS_WK6 = 2 and child.MARKER <> 'O'
GROUP BY season.SEAS_WK6, flu.PATIENT_ZIP3, flu.AGEGROUP, child.MARKER
;

/* check if values add up for a single age group in a single zip3 for season 2 */
SELECT season.SEAS_WK6, flu.PATIENT_ZIP3, flu.AGEGROUP, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = '998' and flu.AGEGROUP = '50-59 YEARS' and season.SEAS_WK6 = 2
;
SELECT season.SEAS_WK6, flu.PATIENT_ZIP3, flu.AGEGROUP, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = '997' and flu.AGEGROUP = '20-29 YEARS' and season.SEAS_WK6 = 2
;
/* values seem to agree with those for a single season */
/* should popstat be summed? */
SELECT season.SEAS_WK6, flu.WEEK, flu.PATIENT_ZIP3, flu.AGEGROUP, sum(flu.ILI_m), sum(flu.popstat)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = '997' and flu.AGEGROUP = '20-29 YEARS' and season.SEAS_WK6 = 2
GROUP BY flu.WEEK
;
/* popstat should not be summed. note: the sum of flu.popstat is not a multiple of the popstat value displayed because popstat values change each calendar year and there are two calendar years represented in a single flu season. the popstat value that is exported will represent the population size in the first of those two calendar years. the values from year to year should not change drastically, so it is okay to use this first popstat value. */


/* Function 3: Pull incidence for child and adult populations by week for the peak +/- 6 wk span across all zip3s (7/9/13) */
SELECT season.SEAS_WK6, flu.WEEK, child.MARKER, sum(flu.ILI_m) 
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SEAS_WK6 <> 0
GROUP BY season.SEAS_WK6, flu.WEEK, child.MARKER
;

/* check that child marker works */
SELECT season.SEAS_WK6, flu.WEEK, child.MARKER, sum(flu.ILI_m) 
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SEAS_WK6 <> 0 and flu.AGEGROUP <> '<2 YEARS'
GROUP BY season.SEAS_WK6, flu.WEEK, child.MARKER
;
/* yes it works - ILI counts in the "O" category were decreased */


/* export data function 1 */
SELECT season.SEAS_WK6, child.MARKER, sum(flu.ILI_m) 
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SEAS_WK6 <> 0
GROUP BY season.SEAS_WK6, child.MARKER
INTO OUTFILE '/tmp/OR_swk6.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

/* export data function 2 */
SELECT season.SEAS_WK6, flu.PATIENT_ZIP3, child.MARKER, flu.AGEGROUP, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 <> "TOT" and season.SEAS_WK6 <> 0 and child.MARKER <> 'O'
GROUP BY season.SEAS_WK6, flu.PATIENT_ZIP3, flu.AGEGROUP, child.MARKER
INTO OUTFILE '/tmp/OR_swk6_zip3.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

/* export data function 3 */
SELECT season.SEAS_WK6, flu.WEEK, child.MARKER, sum(flu.ILI_m) 
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SEAS_WK6 <> 0
GROUP BY season.SEAS_WK6, flu.WEEK, child.MARKER
INTO OUTFILE '/tmp/OR_swk6_week.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;


/* files were moved to SQL_export folder */





