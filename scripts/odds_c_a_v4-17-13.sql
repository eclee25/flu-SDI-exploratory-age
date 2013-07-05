/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 4/17/13
Function: Grab data to draw charts for odds ratios of attack rates between children and adults across weeks for each season and across all seasons. Service facilities: all types, severe = acute & ER, mild = outpatient & office

## from 3/29: change data output to seasons from week 40 of y1 to week 20 of y2

Command Line: mysql -u elizabeth -pbansa11ab odds_child_adult.sql
Data: flu table: SDI
*/

-- grab data for children and adults across weeks for each season
SELECT season.SMALL_SEAS_NUM, child.MARKER, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM <> 0
GROUP BY season.SMALL_SEAS_NUM, child.MARKER
INTO OUTFILE '/tmp/odds_c_a1.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

------- run some checks on season 1 -----
--SELECT sum(ILI_m)
--from flu
--WHERE (YEAR(WEEK) = 2000 OR (YEAR(WEEK) = 2001 and WEEK(WEEK)<40)) and flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and (flu.AGEGROUP = '5-9 YEARS' OR flu.AGEGROUP = '10-14 YEARS' OR flu.AGEGROUP = '15-19 YEARS')
--; -- check on child value

--SELECT sum(ILI_m) from flu
--WHERE (YEAR(WEEK) = 2000 OR (YEAR(WEEK) = 2001 and WEEK(WEEK)<40)) and flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and (flu.AGEGROUP = '<2 YEARS' OR flu.AGEGROUP = '2-4 YEARS' OR flu.AGEGROUP = '60-69 YEARS' OR flu.AGEGROUP = '70-79 YEARS' OR flu.AGEGROUP = '80+ YEARS')
--; -- check on other value

--SELECT sum(ILI_m) from flu
--WHERE (YEAR(WEEK) = 2000 OR (YEAR(WEEK) = 2001 and WEEK(WEEK)<40)) and flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and flu.AGEGROUP = "TOTAL"
--; -- check on total season 1 value

-- grab data for children and adults across weeks for each season for severe cases (acute and ER only)
SELECT season.SMALL_SEAS_NUM, child.MARKER, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE (flu.SERVICE_PLACE = "INPATIENT ACUTE CARE FACILITY" OR flu.SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC") and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM <> 0
GROUP BY season.SMALL_SEAS_NUM, child.MARKER
INTO OUTFILE '/tmp/odds_c_a3_a.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
-- grab data for children and adults across weeks for each season for milder cases (office and outpatient only)
SELECT season.SMALL_SEAS_NUM, child.MARKER, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE (flu.SERVICE_PLACE = "OFFICE/OP CLINICS" OR flu.SERVICE_PLACE = "OUTPATIENT FACILITY") and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM <> 0
GROUP BY season.SMALL_SEAS_NUM, child.MARKER
INTO OUTFILE '/tmp/odds_c_a3_b.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

-------------------------------------------------------
-- grab data for children and adults across all seasons
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.WEEK, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM = 1
GROUP BY season.SMALL_SEAS_NUM, flu.WEEK, child.MARKER
INTO OUTFILE '/tmp/odds_c_a2_a.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.WEEK, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM = 2
GROUP BY season.SMALL_SEAS_NUM, flu.WEEK, child.MARKER
INTO OUTFILE '/tmp/odds_c_a2_b.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.WEEK, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM = 3
GROUP BY season.SMALL_SEAS_NUM, flu.WEEK, child.MARKER
INTO OUTFILE '/tmp/odds_c_a2_c.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.WEEK, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM = 4
GROUP BY season.SMALL_SEAS_NUM, flu.WEEK, child.MARKER
INTO OUTFILE '/tmp/odds_c_a2_d.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.WEEK, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM = 5
GROUP BY season.SMALL_SEAS_NUM, flu.WEEK, child.MARKER
INTO OUTFILE '/tmp/odds_c_a2_e.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.WEEK, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM = 6
GROUP BY season.SMALL_SEAS_NUM, flu.WEEK, child.MARKER
INTO OUTFILE '/tmp/odds_c_a2_f.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.WEEK, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM = 7
GROUP BY season.SMALL_SEAS_NUM, flu.WEEK, child.MARKER
INTO OUTFILE '/tmp/odds_c_a2_g.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.WEEK, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM = 8
GROUP BY season.SMALL_SEAS_NUM, flu.WEEK, child.MARKER
INTO OUTFILE '/tmp/odds_c_a2_h.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.WEEK, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM = 9
GROUP BY season.SMALL_SEAS_NUM, flu.WEEK, child.MARKER
INTO OUTFILE '/tmp/odds_c_a2_i.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT season.SMALL_SEAS_NUM, child.MARKER, flu.WEEK, sum(ILI_m)
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM = 10
GROUP BY season.SMALL_SEAS_NUM, flu.WEEK, child.MARKER
INTO OUTFILE '/tmp/odds_c_a2_j.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
-------run some checks on child values for season 1------
--SELECT season.SMALL_SEAS_NUM, flu.WEEK, sum(ILI_m)
--from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
--WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM = 1 and (flu.AGEGROUP = '5-9 YEARS' OR flu.AGEGROUP = '10-14 YEARS' OR flu.AGEGROUP = '15-19 YEARS')
--GROUP BY season.SMALL_SEAS_NUM, flu.WEEK
--;
--SELECT flu.WEEK, sum(ILI_m)
--from flu 
--WHERE (YEAR(WEEK) = 2000 OR (YEAR(WEEK) = 2001 and WEEK(WEEK)<40)) and flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT"and (flu.AGEGROUP = '5-9 YEARS' OR flu.AGEGROUP = '10-14 YEARS' OR flu.AGEGROUP = '15-19 YEARS')
--GROUP BY flu.WEEK
--;

-------------------------------------------------------------
-- any diagnosis counts: sum by flu season number for children (5-19 yo), adults (20-59 yo), other (0-4, 60-80+ yo)

SELECT season.SMALL_SEAS_NUM, child.MARKER, sum(ANY_DIAG_VISIT_CT)
from flu RIGHT JOIN season on (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and season.SMALL_SEAS_NUM <> 0
GROUP BY season.SMALL_SEAS_NUM, child.MARKER
INTO OUTFILE '/tmp/anydiag.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

---- run checks on any diagnosis counts --

SELECT season.SMALL_SEAS_NUM, child.MARKER, year(flu.week), sum(ANY_DIAG_VISIT_CT)
from flu RIGHT JOIN season on (flu.WEEK = season.WEEK) RIGHT JOIN child ON (child.AGEGROUP = flu.AGEGROUP)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT"
GROUP BY season.SMALL_SEAS_NUM, year(flu.week), child.MARKER
;
SELECT season.SMALL_SEAS_NUM, sum(ANY_DIAG_VISIT_CT) from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and flu.AGEGROUP = "TOTAL"
GROUP BY season.SMALL_SEAS_NUM
; 
SELECT sum(ANY_DIAG_VISIT_CT) from flu 
WHERE SERVICE_PLACE = "TOTAL" and PATIENT_ZIP3 = "TOT" and AGEGROUP = "TOTAL"
;








