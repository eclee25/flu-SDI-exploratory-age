
/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 9/28/12
Function: Export SDI flu data into different shapes to draw general plots

Date: 10/2/12

Command Line: mysql -u elizabeth -pBans1Lab! (run in chunks)
Data: flu table: SDI, stdpop table: http://seer.cancer.gov/stdpopulations/stdpop.singleages.html
*/

--subset data by service place
SELECT AGEGROUP, YEAR(WEEK), sum(ILI_m), sum(ANY_DIAG_VISIT_CT), sum(ILI_m)/sum(ANY_DIAG_VISIT_CT) as ILI_prop FROM flu
WHERE SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC" AND PATIENT_ZIP3 = "TOT" 
GROUP BY AGEGROUP, YEAR(WEEK)
;
--the ILI proportions and counts for the elderly were not increased in emergency room visits, as we expected. In fact, there were lower proportions of the elderly visiting the emergency room due to ILI, likely because they have so many other urgent ailments. There were indeed, however, a greater number of total visits from the elderly than children to the emergency room.

--debugging
SELECT YEAR(WEEK),YEAR(WEEK)-2000 AS x, sign(YEAR(WEEK)-2000) as sign , abs(sign(YEAR(WEEK)-2000)) as abso, 1-abs(sign(YEAR(WEEK)-2000)) as oneminus, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2001)))) as X2001, sum(ILI_m)
from flu 
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND AGEGROUP = "TOTAL" AND (YEAR(WEEK) = 2000 OR YEAR(WEEK) = 2001)
GROUP BY YEAR(WEEK);


--------reshape data for charts 9/28/12----------

--ILI counts by agegroup by year
SELECT AGEGROUP, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2000)))) as ILI_2000, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2001)))) as ILI_2001, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2002)))) as ILI_2002, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2003)))) as ILI_2003, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2004)))) as ILI_2004, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2005)))) as ILI_2005, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2006)))) as ILI_2006, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2007)))) as ILI_2007, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2008)))) as ILI_2008, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2009)))) as ILI_2009, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2010)))) as ILI_2010
from flu 
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND AGEGROUP != "TOTAL"
GROUP BY AGEGROUP;

--all visit counts by agegroup by year
SELECT AGEGROUP, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2000)))) as ANY_2000, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2001)))) as ANY_2001, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2002)))) as ANY_2002, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2003)))) as ANY_2003, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2004)))) as ANY_2004, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2005)))) as ANY_2005, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2006)))) as ANY_2006, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2007)))) as ANY_2007, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2008)))) as ANY_2008, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2009)))) as ANY_2009, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2010)))) as ANY_2010
from flu 
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND AGEGROUP != "TOTAL"
GROUP BY AGEGROUP;

--ILI proportion by agegroup by year
SELECT AGEGROUP, 
sum((ILI_m/ANY_DIAG_VISIT_CT)*(1-abs(sign(YEAR(WEEK)-2000)))) as ILIp_2000, 
sum((ILI_m/ANY_DIAG_VISIT_CT)*(1-abs(sign(YEAR(WEEK)-2001)))) as ILIp_2001, 
sum((ILI_m/ANY_DIAG_VISIT_CT)*(1-abs(sign(YEAR(WEEK)-2002)))) as ILIp_2002, 
sum((ILI_m/ANY_DIAG_VISIT_CT)*(1-abs(sign(YEAR(WEEK)-2003)))) as ILIp_2003, 
sum((ILI_m/ANY_DIAG_VISIT_CT)*(1-abs(sign(YEAR(WEEK)-2004)))) as ILIp_2004, 
sum((ILI_m/ANY_DIAG_VISIT_CT)*(1-abs(sign(YEAR(WEEK)-2005)))) as ILIp_2005, 
sum((ILI_m/ANY_DIAG_VISIT_CT)*(1-abs(sign(YEAR(WEEK)-2006)))) as ILIp_2006, 
sum((ILI_m/ANY_DIAG_VISIT_CT)*(1-abs(sign(YEAR(WEEK)-2007)))) as ILIp_2007, 
sum((ILI_m/ANY_DIAG_VISIT_CT)*(1-abs(sign(YEAR(WEEK)-2008)))) as ILIp_2008, 
sum((ILI_m/ANY_DIAG_VISIT_CT)*(1-abs(sign(YEAR(WEEK)-2009)))) as ILIp_2009, 
sum((ILI_m/ANY_DIAG_VISIT_CT)*(1-abs(sign(YEAR(WEEK)-2010)))) as ILIp_2010
from flu 
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND AGEGROUP != "TOTAL"
GROUP BY AGEGROUP;

----------------------------------------------------------
------ by year (same as above) with binned agegroup 10/2/12--------


	
--ILI counts by agebin by year;
SELECT age_binned.BIN, age_binned.AGEBIN, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2000)))) as ILI_2000, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2001)))) as ILI_2001, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2002)))) as ILI_2002, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2003)))) as ILI_2003, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2004)))) as ILI_2004, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2005)))) as ILI_2005, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2006)))) as ILI_2006, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2007)))) as ILI_2007, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2008)))) as ILI_2008, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2009)))) as ILI_2009, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2010)))) as ILI_2010
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP != "TOTAL"
GROUP BY age_binned.BIN
INTO OUTFILE '/tmp/A1.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

--all visit counts by agebin by year;
SELECT age_binned.BIN, age_binned.AGEBIN, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2000)))) as ANY_2000, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2001)))) as ANY_2001, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2002)))) as ANY_2002, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2003)))) as ANY_2003, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2004)))) as ANY_2004, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2005)))) as ANY_2005, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2006)))) as ANY_2006, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2007)))) as ANY_2007, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2008)))) as ANY_2008, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2009)))) as ANY_2009, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2010)))) as ANY_2010
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP != "TOTAL"
GROUP BY age_binned.BIN
INTO OUTFILE '/tmp/A2.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

--ILI proportion by agegroup by year;
SELECT age_binned.BIN, age_binned.AGEBIN,  
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2000))))/sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2000)))) as ILIp_2000, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2001))))/sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2001)))) as ILIp_2001, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2002))))/sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2002)))) as ILIp_2002,
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2003))))/sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2003)))) as ILIp_2003, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2004))))/sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2004)))) as ILIp_2004, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2005))))/sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2005)))) as ILIp_2005, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2006))))/sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2006)))) as ILIp_2006, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2007))))/sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2007)))) as ILIp_2007, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2008))))/sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2008)))) as ILIp_2008, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2009))))/sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2009)))) as ILIp_2009, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2010))))/sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2010)))) as ILIp_2010 
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP != "TOTAL"
GROUP BY age_binned.BIN
INTO OUTFILE '/tmp/A3.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

-----------------------------------------------
------- year vs peak time chart 10/3/12 --------

--create a new table where week number is linked with dates
--actually, this table wasn't really necessary but good for reference I guess;
USE sdi;
DROP TABLE if exists months;
CREATE TABLE months
AS(SELECT DISTINCT WEEK, YEAR(WEEK) as YEAR, MONTHNAME(WEEK) as MONTH, WEEKOFYEAR(WEEK) as WEEKNUM 
from flu
GROUP BY WEEK
)
;

-- define peak time as weeks where: ILI proportion > .02 for 10-14 year olds. Young children peak prior to the rest of the population so they might be inappropriate to use as a proxy, 10-14 year olds have a peak duration that is in between that of young children and adults; select data that will plot peak week numbers by year;

SELECT WEEK, YEAR(WEEK) as YEAR, MONTHNAME(WEEK) as MONTH, WEEKOFYEAR(WEEK) as WEEKNUM, ILI_m/ANY_DIAG_VISIT_CT as ILI_PROP
from flu
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND AGEGROUP = "10-14 YEARS" AND ILI_m/ANY_DIAG_VISIT_CT > .02
GROUP BY WEEK
INTO OUTFILE '/tmp/B3.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

-------------------------------------------------
------- by week with binned agegroup --------- 
SELECT age_binned.BIN, age_binned.AGEBIN, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2000)))) as ILI_2000, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2001)))) as ILI_2001, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2002)))) as ILI_2002, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2003)))) as ILI_2003, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2004)))) as ILI_2004, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2005)))) as ILI_2005, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2006)))) as ILI_2006, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2007)))) as ILI_2007, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2008)))) as ILI_2008, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2009)))) as ILI_2009, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2010)))) as ILI_2010
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP != "TOTAL"
GROUP BY age_binned.BIN
INTO OUTFILE '/tmp/A1.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

--------------------------------------------------------
------ILI counts at the ER by agebin-------
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "<2 YEARS"
GROUP BY age_binned.BIN, WEEK
INTO OUTFILE '/tmp/D1a.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "5-9 YEARS" OR flu.AGEGROUP = "10-14 YEARS" OR flu.AGEGROUP = "15-19 YEARS")
GROUP BY age_binned.BIN, WEEK
INTO OUTFILE '/tmp/D1c.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "20-29 YEARS"
GROUP BY age_binned.BIN, WEEK
INTO OUTFILE '/tmp/D1d.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "50-59 YEARS" OR flu.AGEGROUP = "60-69 YEARS")
GROUP BY age_binned.BIN, WEEK
INTO OUTFILE '/tmp/D1f.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "5-9 YEARS" OR flu.AGEGROUP = "10-14 YEARS" OR flu.AGEGROUP = "15-19 YEARS")
GROUP BY age_binned.BIN, WEEK
INTO OUTFILE '/tmp/E1c.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "50-59 YEARS" OR flu.AGEGROUP = "60-69 YEARS")
GROUP BY age_binned.BIN, WEEK
INTO OUTFILE '/tmp/E1f.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

--NEED TO WORK ON THIS: PEAK WEEK FOR EACH SEASON******
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, YEAR(WEEK), WEEKOFYEAR(WEEK) as WKOFYR, max(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "TOTAL" AND ILI_m=(select max(ILI_m) from flu WHERE YEAR(WEEK)="2001")
INTO OUTFILE '/tmp/F1_2001.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, YEAR(WEEK), WEEKOFYEAR(WEEK) as WKOFYR, max(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "TOTAL" AND ILI_m=(select max(ILI_m) from flu WHERE YEAR(WEEK)="2002")
INTO OUTFILE '/tmp/F1_2002.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, YEAR(WEEK), WEEKOFYEAR(WEEK) as WKOFYR, max(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "TOTAL" AND ILI_m=(select max(ILI_m) from flu WHERE YEAR(WEEK)="2003" AND WEEKOFYEAR(WEEK)<20)
INTO OUTFILE '/tmp/F1_2003.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, YEAR(WEEK), WEEKOFYEAR(WEEK) as WKOFYR, max(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "TOTAL" AND ILI_m=(select max(ILI_m) from flu WHERE YEAR(WEEK)="2003" AND WEEKOFYEAR(WEEK)>19)
INTO OUTFILE '/tmp/F1_2004.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, YEAR(WEEK), WEEKOFYEAR(WEEK) as WKOFYR, max(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "TOTAL" AND ILI_m=(select max(ILI_m) from flu WHERE YEAR(WEEK)="2005")
INTO OUTFILE '/tmp/F1_2005.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, YEAR(WEEK), WEEKOFYEAR(WEEK) as WKOFYR, max(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "TOTAL" AND ILI_m=(select max(ILI_m) from flu WHERE YEAR(WEEK)="2006")
INTO OUTFILE '/tmp/F1_2006.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, YEAR(WEEK), WEEKOFYEAR(WEEK) as WKOFYR, max(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "TOTAL" AND ILI_m=(select max(ILI_m) from flu WHERE YEAR(WEEK)="2007")
INTO OUTFILE '/tmp/F1_2007.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, YEAR(WEEK), WEEKOFYEAR(WEEK) as WKOFYR, max(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "TOTAL" AND ILI_m=(select max(ILI_m) from flu WHERE YEAR(WEEK)="2008")
INTO OUTFILE '/tmp/F1_2008.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, YEAR(WEEK), WEEKOFYEAR(WEEK) as WKOFYR, max(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "TOTAL" AND ILI_m=(select max(ILI_m) from flu WHERE YEAR(WEEK)="2009" AND WEEKOFYEAR(WEEK)<20)
INTO OUTFILE '/tmp/F1_2009.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, YEAR(WEEK), WEEKOFYEAR(WEEK) as WKOFYR, max(ILI_m)
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "TOTAL" AND ILI_m=(select max(ILI_m) from flu WHERE YEAR(WEEK)="2009" AND WEEKOFYEAR(WEEK)>19)
INTO OUTFILE '/tmp/F1_2009pan.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

--US population 2000
SELECT AGEBIN, sum(STDPOP_2000) from stdpop
GROUP BY AGEBIN
;

----------------------------------------------------------
------ILI counts at ER by agebin normalized by population-------
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000), sum(ILI_m)/sum(stdpop.STDPOP_2000)*10000 as ILI_norm_by_10000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "<2 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/D4a.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000), sum(ILI_m)/sum(stdpop.STDPOP_2000)*10000 as ILI_norm_by_10000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "2-4 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/D4b.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000)/3, sum(ILI_m)/(sum(stdpop.STDPOP_2000)/3)*10000 as ILI_norm_by_10000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "5-9 YEARS" OR flu.AGEGROUP = "10-14 YEARS" OR flu.AGEGROUP = "15-19 YEARS") AND stdpop.AGEBIN = "5-19 YEARS"
GROUP BY age_binned.AGEBIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/D4c.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000),sum(ILI_m)/sum(stdpop.STDPOP_2000)*10000 as ILI_norm_by_10000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "20-29 YEARS" AND stdpop.AGEBIN = "20-29 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/D4d.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000)/2, sum(ILI_m)/(sum(stdpop.STDPOP_2000)/2)*10000 as ILI_norm_by_10000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "30-39 YEARS" OR flu.AGEGROUP = "40-49 YEARS") AND stdpop.AGEBIN = "30-49 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/D4e.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000)/2, sum(ILI_m)/(sum(stdpop.STDPOP_2000)/2)*10000 as ILI_norm_by_10000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "50-59 YEARS" OR flu.AGEGROUP = "60-69 YEARS") AND stdpop.AGEBIN = "50-69 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/D4f.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000)/2, sum(ILI_m)/(sum(stdpop.STDPOP_2000)/2)*10000 as ILI_norm_by_10000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "70-79 YEARS" OR flu.AGEGROUP = "80+ YEARS") AND stdpop.AGEBIN = "70+ YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/D4g.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

----------------------------------------------------------
------ILI counts all locations by agebin per population-------
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000), sum(ILI_m)/sum(stdpop.STDPOP_2000)*100000 as ILI_norm_by_100000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "<2 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/E4a.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000), sum(ILI_m)/sum(stdpop.STDPOP_2000)*100000 as ILI_norm_by_100000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "2-4 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/E4b.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000)/3, sum(ILI_m)/(sum(stdpop.STDPOP_2000)/3)*100000 as ILI_norm_by_100000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "5-9 YEARS" OR flu.AGEGROUP = "10-14 YEARS" OR flu.AGEGROUP = "15-19 YEARS") AND stdpop.AGEBIN = "5-19 YEARS"
GROUP BY age_binned.AGEBIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/E4c.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000),sum(ILI_m)/sum(stdpop.STDPOP_2000)*100000 as ILI_norm_by_100000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "20-29 YEARS" AND stdpop.AGEBIN = "20-29 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/E4d.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000)/2, sum(ILI_m)/(sum(stdpop.STDPOP_2000)/2)*100000 as ILI_norm_by_100000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "30-39 YEARS" OR flu.AGEGROUP = "40-49 YEARS") AND stdpop.AGEBIN = "30-49 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/E4e.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000)/2, sum(ILI_m)/(sum(stdpop.STDPOP_2000)/2)*100000 as ILI_norm_by_100000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "50-59 YEARS" OR flu.AGEGROUP = "60-69 YEARS") AND stdpop.AGEBIN = "50-69 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/E4f.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000)/2, sum(ILI_m)/(sum(stdpop.STDPOP_2000)/2)*100000 as ILI_norm_by_100000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "70-79 YEARS" OR flu.AGEGROUP = "80+ YEARS") AND stdpop.AGEBIN = "70+ YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/E4g.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;


----------------------------------------------------------
------ILI counts at inpatient acute care facility by agebin normalized by population-------
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000), sum(ILI_m)/sum(stdpop.STDPOP_2000)*10000 as ILI_norm_by_10000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEGROUP)
WHERE SERVICE_PLACE = "INPATIENT ACUTE CARE FACILITY" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "<2 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/G4a.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000), sum(ILI_m)/sum(stdpop.STDPOP_2000)*10000 as ILI_norm_by_10000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "INPATIENT ACUTE CARE FACILITY" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "2-4 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/G4b.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000)/3, sum(ILI_m)/(sum(stdpop.STDPOP_2000)/3)*10000 as ILI_norm_by_10000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "INPATIENT ACUTE CARE FACILITY" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "5-9 YEARS" OR flu.AGEGROUP = "10-14 YEARS" OR flu.AGEGROUP = "15-19 YEARS") AND stdpop.AGEBIN = "5-19 YEARS"
GROUP BY age_binned.AGEBIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/G4c.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000),sum(ILI_m)/sum(stdpop.STDPOP_2000)*10000 as ILI_norm_by_10000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "INPATIENT ACUTE CARE FACILITY" AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP = "20-29 YEARS" AND stdpop.AGEBIN = "20-29 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/G4d.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000)/2, sum(ILI_m)/(sum(stdpop.STDPOP_2000)/2)*10000 as ILI_norm_by_10000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "INPATIENT ACUTE CARE FACILITY" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "30-39 YEARS" OR flu.AGEGROUP = "40-49 YEARS") AND stdpop.AGEBIN = "30-49 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/G4e.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000)/2, sum(ILI_m)/(sum(stdpop.STDPOP_2000)/2)*10000 as ILI_norm_by_10000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "INPATIENT ACUTE CARE FACILITY" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "50-59 YEARS" OR flu.AGEGROUP = "60-69 YEARS") AND stdpop.AGEBIN = "50-69 YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/G4f.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
SELECT age_binned.BIN, age_binned.AGEBIN, WEEK, WEEKOFYEAR(WEEK) as WKOFYR, sum(ILI_m), sum(stdpop.STDPOP_2000)/2, sum(ILI_m)/(sum(stdpop.STDPOP_2000)/2)*10000 as ILI_norm_by_10000
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP) RIGHT JOIN stdpop on (stdpop.AGEBIN = age_binned.AGEBIN)
WHERE SERVICE_PLACE = "INPATIENT ACUTE CARE FACILITY" AND PATIENT_ZIP3= "TOT" AND (flu.AGEGROUP = "70-79 YEARS" OR flu.AGEGROUP = "80+ YEARS") AND stdpop.AGEBIN = "70+ YEARS"
GROUP BY age_binned.BIN, stdpop.AGEBIN, WEEK
INTO OUTFILE '/tmp/G4g.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

--EXPLORATION--

-----------------do the elderly more often visit the emergency rooms with ILI cases?-------------------------

SELECT age_binned.BIN, age_binned.AGEBIN, SERVICE_PLACE,
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2000)))) as ILI_2000, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2001)))) as ILI_2001, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2002)))) as ILI_2002, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2003)))) as ILI_2003, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2004)))) as ILI_2004, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2005)))) as ILI_2005, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2006)))) as ILI_2006, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2007)))) as ILI_2007, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2008)))) as ILI_2008, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2009)))) as ILI_2009, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2010)))) as ILI_2010
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE (flu.AGEGROUP="50-59 YEARS" OR flu.AGEGROUP="60-69 YEARS" OR flu.AGEGROUP="70-79 YEARS" OR flu.AGEGROUP="80+ YEARS") AND PATIENT_ZIP3= "TOT" AND flu.AGEGROUP != "TOTAL"
GROUP BY AGEBIN; --the elderly do not visit emergency rooms in higher proportions due to ILI symptoms as compared to other service places

SELECT age_binned.BIN, age_binned.AGEBIN, SERVICE_PLACE,
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2000)))) as ILI_2000, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2001)))) as ILI_2001, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2002)))) as ILI_2002, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2003)))) as ILI_2003, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2004)))) as ILI_2004, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2005)))) as ILI_2005, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2006)))) as ILI_2006, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2007)))) as ILI_2007, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2008)))) as ILI_2008, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2009)))) as ILI_2009, 
sum(ILI_m*(1-abs(sign(YEAR(WEEK)-2010)))) as ILI_2010
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE PATIENT_ZIP3= "TOT" AND flu.AGEGROUP != "TOTAL" AND SERVICE_PLACE= "EMERGENCY ROOM/URGENT CARE FAC"
GROUP BY AGEBIN; --the elderly do not visit emergency rooms with ILI symptoms at greater frequency than other age groups. In fact, it would appear that young children visit there at the highest counts

SELECT age_binned.BIN, age_binned.AGEBIN, SERVICE_PLACE,
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2000)))) as ANY_2000, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2001)))) as ANY_2001, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2002)))) as ANY_2002, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2003)))) as ANY_2003, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2004)))) as ANY_2004, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2005)))) as ANY_2005, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2006)))) as ANY_2006, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2007)))) as ANY_2007, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2008)))) as ANY_2008, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2009)))) as ANY_2009, 
sum(ANY_DIAG_VISIT_CT*(1-abs(sign(YEAR(WEEK)-2010)))) as ANY_2010
from flu RIGHT JOIN age_binned ON (flu.AGEGROUP = age_binned.AGEGROUP)
WHERE PATIENT_ZIP3= "TOT" AND flu.AGEGROUP != "TOTAL"
GROUP BY age_binned.BIN; --the elderly visit the emergency room in greater numbers for all types of diseases, which probably explains why the proportion that visit with ILI symptoms is small

