/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 5/16/13
Function: Grab data to draw charts for odds ratios by zipcode of attack rates between children and adults across weeks for each season and across all seasons. 

Command Line: mysql -u elizabeth -pbansa11ab OR_zipcode_v5-16-13.sql
Data: flu table: SDI
*/

-- identify zipcodes that will be included --
select distinct patient_zip3, popstat from flu where popstat = ' ';
-- there were 52 zipcodes that had missing values for at least one row in popstat 
-- compare this list of 52 to http://en.wikipedia.org/wiki/List_of_ZIP_code_prefixes locations. Many zipcodes belong to the IRS, government, military, or US territories, or are otherwise not in use in a normal way
-- of these 52 zipcodes, the following should be explored further because they appear to be normal zipcodes that should have valid data (311, 332, 398, 509, 555, 753, 772, 851, 872, 885, 889, 901, 942)
-- 311, 332, 509, 555, 753, 772, 872, 885, 889, 901, 942: all missing popstat
-- 398: missing 2002 popstat but not in other years
-- 851: missing popstat across multiple months in multiple years but none are missing in 2010
-- SO-- of the 52 zipcode prefixes that have any missing popstat values, include 398 and 851 only
select patient_zip3, week, agegroup, sum(ILI_m), popstat from flu where (patient_zip3 = 311) and popstat <> ' ' 
group by patient_zip3, week, agegroup
;
-- create a table that is a list of zipcode prefixes that will be completely dropped from our analysis (See create_popstatdrop.sql in /Dropbox/Elizabeth_Bansal_Lab/SDI_Data/scripts/admin/


SELECT distinct PATIENT_ZIP3 from flu
INTO OUTFILE '/tmp/pskeep.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
-- create a table that is a list of only zipcode prefixes that will be included in our zipcode level analysis (See create_pskeep.sql in /Dropbox/Elizabeth_Bansal_Lab/SDI_Data/scripts/admin/)
-- this seems easier to implement than the popstatdrop analysis
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.WEEK, flu.PATIENT_ZIP3, sum(ILI_m)
from flu, popstatdrop RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and popstatdrop.ZIP3 <> flu.PATIENT_ZIP3 and season.SMALL_SEAS_NUM = 1
GROUP BY season.SMALL_SEAS_NUM, flu.WEEK, child.MARKER
;
SELECT patient_zip3, popstat from flu, popstatdrop where flu.patient_zip3 = popstatdrop.zip3 and flu.SERVICE_PLACE = "TOTAL" and flu.AGEGROUP = "TOTAL";
SELECT distinct flu.PATIENT_ZIP3 from flu, popstatdrop WHERE flu.PATIENT_ZIP3 <> popstatdrop.ZIP3;


---------------------------------
------exploratory work----------
select distinct agegroup from flu where week = "2001-04-08" and patient_zip3 = "992";
select distinct agegroup from flu where week = "2001-04-08" and patient_zip3 = "997";

SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.WEEK, pskeep.ZIP3, sum(flu.ILI_m), sum(flu.popstat)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP) RIGHT JOIN pskeep ON (pskeep.ZIP3 = flu.PATIENT_ZIP3) 
WHERE flu.SERVICE_PLACE = "TOTAL" and season.SMALL_SEAS_NUM = 1 and (flu.week = "2001-04-08" or flu.week = "2001-04-15") and (flu.patient_zip3 = "992" or flu.patient_zip3 = "997")
GROUP BY season.SMALL_SEAS_NUM, flu.WEEK, pskeep.ZIP3, child.MARKER
;

select year(flu.week) as year, pskeep.zip3, flu.agegroup, child.marker, flu.popstat from flu right join pskeep on (pskeep.zip3 = flu.patient_zip3) right join child on (child.agegroup = flu.agegroup)
where flu.service_place = "TOTAL" and year(flu.week) = 2002 and (flu.patient_zip3 = "366" or flu.patient_zip3 = "397")
group by year(flu.week), pskeep.zip3, flu.agegroup
;
select flu.week, patient_zip3, flu.agegroup, sum(ILI_m), flu.popstat, sum(popstat) from flu where flu.service_place = "TOTAL" and agegroup = "40-49 YEARS" and (flu.patient_zip3 = "397")
group by patient_zip3, flu.week
; --check on specific entries from the table produced from the code above

select flu.week, patient_zip3, flu.agegroup, sum(ILI_m), flu.popstat, sum(popstat) from flu where flu.service_place = "TOTAL" and agegroup = "40-49 YEARS" and (flu.patient_zip3 = "397")
group by patient_zip3, flu.week
; -- there is no 2002 data either in ILI_m or popstat for prefix 397 and 40-49 year olds

-------------------------------------------
-- create a table with year, zip3, childmarker, sum(popstat) to use as a reference for age-specific population within a zipcode prefix.
select year(flu.week) as year, pskeep.zip3, child.marker, flu.agegroup, flu.popstat from flu right join pskeep on (pskeep.zip3 = flu.patient_zip3) right join child on (child.agegroup = flu.agegroup)
where flu.service_place = "TOTAL" and (year(flu.week) = 2002 or year(flu.week) = 2003) and (flu.patient_zip3 = "397" or flu.patient_zip3 = "402")
group by year(flu.week), pskeep.zip3, child.marker, flu.agegroup
;

/* Given the below format of dataset (generated from code above), how can we summarize popstat by year, zipcode, and child.marker (instead of agegroup)?

 year | zip3 | marker | agegroup    | popstat |
+------+------+--------+-------------+---------+
| 2002 | 397  | A      | 20-29 YEARS |   29480 |
| 2002 | 397  | A      | 30-39 YEARS |   21916 |
| 2002 | 397  | A      | 50-59 YEARS |   18108 |
| 2002 | 397  | C      | 10-14 YEARS |   13318 |
| 2002 | 397  | C      | 15-19 YEARS |   15792 |
| 2002 | 397  | C      | 5-9 YEARS   |   12284 |
| 2002 | 397  | O      | 2-4 YEARS   |    7255 |
| 2002 | 397  | O      | 70-79 YEARS |    8418 |
| 2002 | 397  | O      | 80+ YEARS   |    5901 |
| 2002 | 397  | O      | <2 YEARS    |    4805 |
| 2002 | 402  | A      | 20-29 YEARS |   92591 |
| 2002 | 402  | A      | 30-39 YEARS |  100270 |
| 2002 | 402  | A      | 40-49 YEARS |  110525 |
| 2002 | 402  | A      | 50-59 YEARS |   82220 |
| 2002 | 402  | C      | 10-14 YEARS |   47066 |
| 2002 | 402  | C      | 15-19 YEARS |   45022 |
| 2002 | 402  | C      | 5-9 YEARS   |   46246 |
| 2002 | 402  | O      | 2-4 YEARS   |   27239 |
| 2002 | 402  | O      | 60-69 YEARS |   52571 |
| 2002 | 402  | O      | 70-79 YEARS |   42521 |
| 2002 | 402  | O      | 80+ YEARS   |   24764 |
| 2002 | 402  | O      | <2 YEARS    |   18535 |

intermediate table
select year, zip3, marker, sum(popstat) from tablename
group by year, zip3, marker
;

*/

-- code to generate table needed, execute as script and export as csv. import csv into mysql as a new table. run 'intermediate table' select statement to generate the reference table that will have the popstat values for each zipcode, year, and binned age group. ECL 5/17/13
select year(flu.week) as year, pskeep.zip3, child.marker, flu.agegroup, flu.popstat from flu right join pskeep on (pskeep.zip3 = flu.patient_zip3) right join child on (child.agegroup = flu.agegroup)
where flu.service_place = "TOTAL"
group by year(flu.week), pskeep.zip3, child.marker, flu.agegroup
INTO OUTFILE '/tmp/psref_int.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

--- grab popstat for all ages in each zipcode prefix in order to draw a histogram of the distribution of the populations in the zipcodes
select year(week), patient_zip3, popstat from flu where year(week) = 2010 and agegroup = "TOTAL" and service_place = "TOTAL" 
group by patient_zip3
INTO OUTFILE '/tmp/popstat_by_zip3_2010.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

-------------------------------------------------------
-- grab ILI_m data for children and adults across all seasons and zipcodes

SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.patient_zip3, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 <> "TOT" and season.SMALL_SEAS_NUM <> 0
GROUP BY season.SMALL_SEAS_NUM, flu.PATIENT_ZIP3, child.MARKER
; -- some popstats == 0 so they need to be removed

SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.patient_zip3, sum(flu.ILI_m), sum(flu.popstat)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 <> "TOT" and flu.popstat <> 0 and  flu.PATIENT_ZIP3 = "901"
GROUP BY season.SMALL_SEAS_NUM, child.MARKER
; -- the flu.popstat <> 0 command works and removes rows where popstat == 0
-- 6/12/13 error: sum(flu.popstat) changed to flu.popstat

SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.patient_zip3, sum(flu.ILI_m), sum(flu.popstat)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 <> "TOT" and flu.popstat <> 0
GROUP BY season.SMALL_SEAS_NUM, flu.patient_zip3, child.MARKER
INTO OUTFILE '/tmp/zipcode_bysseas.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
; -- small season number = 0 needs to be dropped


---- 6/12/13 examine how many zip3s are afflicted with underestimation of population size due to missing 5-yr age group popstat data when we sum popstat by agegroup marker. this issue leads to an overestimation of attack rates -- is there a systematic bias for overestimating attack rates in one age group vs another age group?
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.patient_zip3, flu.AGEGROUP, sum(flu.ILI_m), sum(flu.popstat)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 <> "TOT" and flu.popstat <> 0 and season.SMALL_SEAS_NUM = 1 and child.MARKER <> 'O'
GROUP BY season.SMALL_SEAS_NUM, flu.patient_zip3, child.MARKER, flu.AGEGROUP
; -- should not be sum(flu.popstat), instead should be flu.popstat
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.patient_zip3, flu.AGEGROUP, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.popstat <> 0 and season.SMALL_SEAS_NUM = 1 and child.MARKER <> 'O'
GROUP BY season.SMALL_SEAS_NUM, flu.patient_zip3, child.MARKER, flu.AGEGROUP
;
-- compare the sums of popstat for children and adults in a recent season with the US populations of children and adults as identified by the 2010 Census
-- census value for adults = 168392074; 2008 popstat value for adults = 168069825; difference = 322249; % missing = 0.19%
-- census value for children = 63066194; 2008 popstat value for children = 61973769; difference = 1092425; % missing = 1.73%
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.patient_zip3, flu.AGEGROUP, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.popstat <> 0 and season.SMALL_SEAS_NUM = 9 and child.MARKER <> 'O' and flu.patient_zip3 = "TOT"
GROUP BY season.SMALL_SEAS_NUM, flu.patient_zip3, child.MARKER, flu.AGEGROUP
;
-- census value for adults = 168392074; 2009 popstat value for adults = 168393700; difference = -1626; % missing (abs val) = .001%
-- census value for children = 63066194; 2009 popstat value for children = 62043333; difference = 1022861; % missing (abs val) = 1.6%
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.patient_zip3, flu.AGEGROUP, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.popstat <> 0 and season.SMALL_SEAS_NUM = 10 and child.MARKER <> 'O' and flu.patient_zip3 = "TOT"
GROUP BY season.SMALL_SEAS_NUM, flu.patient_zip3, child.MARKER, flu.AGEGROUP
;
-- it would appear that there is more missing data for children than for adults

-- export new data with correct popstat values
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.patient_zip3, flu.AGEGROUP, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.popstat <> 0 and child.MARKER <> 'O'
GROUP BY season.SMALL_SEAS_NUM, flu.patient_zip3, child.MARKER, flu.AGEGROUP
INTO OUTFILE '/tmp/zipcode_bysseas_6-12-13.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;












