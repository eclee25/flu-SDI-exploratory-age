/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 8/25/14
Function: Export any diagnoses during fall (wks 40-46) and summer baselines (wks 33-39) for each season for supplement figure by same name.

outputfile = fall_summer_baselinebars.csv

Command Line: mysql < fall_summer_baselinebars.sql | sed 's/\t/,/g' > fall_summer_baselinebars.csv

Data: flu table: SDI
*/


SELECT season.SEASON_NUM as SNUM, flu.WEEK, year(flu.WEEK) as YEAR, week(flu.WEEK) as WKNUM, sum(ANY_DIAG_VISIT_CT) as ANYDIAG
from flu right join season on (flu.week = season.week)
where flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and flu.AGEGROUP = "TOTAL" and week(flu.WEEK) >= 33 and week(flu.WEEK) <= 46
group by season.SEASON_NUM, flu.WEEK
;




