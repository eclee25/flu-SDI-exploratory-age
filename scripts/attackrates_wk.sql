/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 8/7/13
Function: extract attack rates for entire population by week and include season denominations

Command Line: mysql -u elizabeth -pbansa11ab sdi <attackrates_wk.sql
Data: flu table: SDI
*/

SELECT season.SMALL_SEAS_NUM, flu.WEEK, sum(flu.ILI_m)
from flu right join season on (flu.week = season.week)
where flu.SERVICE_PLACE = "TOTAL" and flu.PATIENT_ZIP3 = "TOT" and flu.AGEGROUP = "TOTAL" and season.SMALL_SEAS_NUM <> 0
group by season.SMALL_SEAS_NUM, flu.WEEK
INTO OUTFILE '/tmp/AR_wk.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

select year(week), popstat from flu 
where patient_zip3 = "TOT" and agegroup = "TOTAL" and service_place = "TOTAL" 
group by year(week)
INTO OUTFILE '/tmp/totalpop.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

-- denominator for attack rates
+------------+-----------+
| year(week) | popstat   |
+------------+-----------+
|       2000 | 274676144 |
|       2001 | 283987704 |
|       2002 | 286776721 |
|       2003 | 290637947 |
|       2004 | 292927888 |
|       2005 | 295132821 |
|       2006 | 298012768 |
|       2007 | 300961101 |
|       2008 | 304009593 |
|       2009 | 306500542 |
|       2010 | 308907497 |
+------------+-----------+





