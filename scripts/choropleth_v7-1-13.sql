-- export data by week, zip3, ILI, popstat value

SELECT season.SEASON_NUM, flu.WEEK, flu.patient_zip3, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.AGEGROUP = "TOTAL"
GROUP BY season.SEASON_NUM, flu.WEEK, flu.patient_zip3
INTO OUTFILE '/tmp/choropleth_v7-1-13.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
-- sum ILI_m not needed

-- check
SELECT season.SEASON_NUM, flu.WEEK, flu.patient_zip3, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.AGEGROUP = "TOTAL" and flu.WEEK = '2009-10-04' and flu.patient_zip3 = '999'
GROUP BY season.SEASON_NUM, flu.WEEK, flu.patient_zip3;

SELECT season.SEASON_NUM, flu.WEEK, flu.patient_zip3, flu.ILI_m, flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.AGEGROUP = "TOTAL" and flu.WEEK = '2009-10-04' and flu.patient_zip3 = '999'
GROUP BY season.SEASON_NUM, flu.WEEK, flu.patient_zip3;

-- check
SELECT season.SEASON_NUM, flu.WEEK, flu.patient_zip3, flu.AGEGROUP, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE = "TOTAL" and flu.WEEK = '2009-10-04' and flu.patient_zip3 = '999'
GROUP BY season.SEASON_NUM, flu.WEEK, flu.patient_zip3, flu.AGEGROUP;

SELECT season.SEASON_NUM, flu.WEEK, flu.patient_zip3, flu.AGEGROUP, sum(flu.ILI_m), flu.popstat
from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.SERVICE_PLACE <> "TOTAL" and flu.WEEK = '2009-10-04' and flu.patient_zip3 = '999'
GROUP BY season.SEASON_NUM, flu.WEEK, flu.patient_zip3, flu.AGEGROUP;

SELECT flu.WEEK, flu.patient_zip3, flu.AGEGROUP, flu.SERVICE_PLACE, flu.ILI_m, flu.popstat
from flu
WHERE flu.WEEK = '2009-10-04' and flu.patient_zip3 = '999'
GROUP BY flu.patient_zip3, flu.AGEGROUP;