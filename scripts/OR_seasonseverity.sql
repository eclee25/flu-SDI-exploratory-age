/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 7/25/13
Function: Grab data that can serve as a proxy for season severity
1) ILI cases over entire population during peak weeks
2) ILI cases over entire population during flu season (Oct to May)
3) ILI cases in acute care facilities during peak weeks
4) ILI cases in ERs during peak weeks
5) ILI cases in acute care facilities during flu season

Decided that ILI cases in acute care facilities during peak weeks seem to best match the information 
Data export: explore/SQL_export/seasonseverity.csv (7/25/13)

Command Line: mysql -u elizabeth -pbansa11ab mysqltemplate.sql
Data: flu table: SDI
*/

/*1) ILI cases over entire population during peak weeks*/
SELECT season.SEAS_WK6, sum(flu.ILI_m), flu.POPSTAT, sum(flu.ILI_m)/flu.POPSTAT*10000 as AR10000 from flu  INNER JOIN season USING (WEEK)
WHERE flu.PATIENT_ZIP3 = "TOT" and flu.AGEGROUP = "TOTAL" and flu.SERVICE_PLACE = "TOTAL" and season.SEAS_WK6 <> 0
GROUP BY season.SEAS_WK6
;
  SEAS_WK6 | sum(flu.ILI_m) | POPSTAT   | AR10000  |
+----------+----------------+-----------+----------+
|        1 |         325403 | 274676144 |  11.8468 |
|        2 |         492800 | 283987704 |  17.3529 |
|        3 |         550100 | 286776721 |  19.1822 |
|        4 |         924041 | 290637947 |  31.7935 |
|        5 |        1066066 | 295132821 |  36.1216 |
|        6 |         781598 | 298012768 |  26.2270 |
|        7 |         830482 | 300961101 |  27.5943 |
|        8 |        1518474 | 304009593 |  49.9482 |
|        9 |        1177879 | 306500542 |  38.4299 |
|       10 |        3166094 | 306500542 | 103.2982 |

/* This metric seems okay, but season 7 should be relatively mild compared to the previous three season. Season 5 had the vax shortage, so perhaps that caused an increase in the attack rate? */


/*2) ILI cases over entire population during flu season (Oct to May)*/
SELECT season.SMALL_SEAS_NUM, sum(flu.ILI_m), flu.POPSTAT, sum(flu.ILI_m)/flu.POPSTAT*10000 as AR10000 from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.PATIENT_ZIP3 = "TOT" and flu.AGEGROUP = "TOTAL" and flu.SERVICE_PLACE = "TOTAL" and season.SMALL_SEAS_NUM <> 0
GROUP BY season.SMALL_SEAS_NUM
;
 SMALL_SEAS_NUM | sum(flu.ILI_m) | POPSTAT   | AR10000  |
+----------------+----------------+-----------+----------+
|              1 |         452312 | 274676144 |  16.4671 |
|              2 |         871832 | 283987704 |  30.6996 |
|              3 |         978677 | 286776721 |  34.1268 |
|              4 |        1485711 | 290637947 |  51.1190 |
|              5 |        1763132 | 292927888 |  60.1900 |
|              6 |        1481798 | 295132821 |  50.2078 |
|              7 |        1550142 | 298012768 |  52.0160 |
|              8 |        2381998 | 300961101 |  79.1464 |
|              9 |        2314294 | 304009593 |  76.1257 |
|             10 |        4601514 | 306500542 | 150.1307 |

/* Increasing the length of the season seems to increase the attack rates by similar proportions, so this metric doesn't seem that useful */


/*3) ILI cases in acute care facilities during peak weeks*/
SELECT season.SEAS_WK6, sum(flu.ILI_m), flu.POPSTAT, sum(flu.ILI_m)/flu.POPSTAT*100000 as AR100000 from flu  INNER JOIN season USING (WEEK)
WHERE flu.PATIENT_ZIP3 = "TOT" and flu.AGEGROUP = "TOTAL" and flu.SERVICE_PLACE = "INPATIENT ACUTE CARE FACILITY" and season.SEAS_WK6 <> 0
GROUP BY season.SEAS_WK6
INTO OUTFILE '/tmp/seasonseverity.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;
 SEAS_WK6 | sum(flu.ILI_m) | POPSTAT   | AR100000 |
+----------+----------------+-----------+----------+
|        1 |           5326 | 274676144 |   1.9390 |
|        2 |          12638 | 283987704 |   4.4501 |
|        3 |          10712 | 286776721 |   3.7353 |
|        4 |          46329 | 290637947 |  15.9404 |
|        5 |          44074 | 295132821 |  14.9336 |
|        6 |          28612 | 298012768 |   9.6009 |
|        7 |          19924 | 300961101 |   6.6201 |
|        8 |          51779 | 304009593 |  17.0320 |
|        9 |          28380 | 306500542 |   9.2593 |
|       10 |         102714 | 306500542 |  33.5118 |

/* This seems to be a pretty good measure of severity. CDC indicates that season 3 and 7 were fairly mild, that season 8 was more severe than the previous three seasons and similar in severity to season 5. The population in acute care facilities doesn't seem to be affected by the vax shortage in season 5 as much, possibly because these individuals would have been high priorities to receive vaccine. Do we want this to reflect season severity independent of vaccine-related artifacts? */


/*4) ILI cases in ERs during peak weeks*/
SELECT season.SEAS_WK6, sum(flu.ILI_m), flu.POPSTAT, sum(flu.ILI_m)/flu.POPSTAT*100000 as AR100000 from flu  INNER JOIN season USING (WEEK)
WHERE flu.PATIENT_ZIP3 = "TOT" and flu.AGEGROUP = "TOTAL" and flu.SERVICE_PLACE = "EMERGENCY ROOM/URGENT CARE FAC" and season.SEAS_WK6 <> 0
GROUP BY season.SEAS_WK6
;
SEAS_WK6 | sum(flu.ILI_m) | POPSTAT   | AR100000 |
+----------+----------------+-----------+----------+
|        1 |          21590 | 274676144 |   7.8601 |
|        2 |          41139 | 283987704 |  14.4861 |
|        3 |          40738 | 286776721 |  14.2054 |
|        4 |          99688 | 290637947 |  34.2997 |
|        5 |         100715 | 295132821 |  34.1253 |
|        6 |          84150 | 298012768 |  28.2370 |
|        7 |          89425 | 300961101 |  29.7131 |
|        8 |         188108 | 304009593 |  61.8756 |
|        9 |         154405 | 306500542 |  50.3767 |
|       10 |         427358 | 306500542 | 139.4314 |

/* This metric is similar to the acute care facilities during peak weeks, except there is a much higher AR in season 9, possibly due to pH1N1. The ARs are also higher in general, which may be noise because ERs are a catch-all for severe patients and individuals without health  */


/*5) ILI cases in acute care facilities during flu season*/
SELECT season.SMALL_SEAS_NUM, sum(flu.ILI_m), flu.POPSTAT, sum(flu.ILI_m)/flu.POPSTAT*100000 as AR100000 from flu RIGHT JOIN season ON (flu.WEEK = season.WEEK)
WHERE flu.PATIENT_ZIP3 = "TOT" and flu.AGEGROUP = "TOTAL" and flu.SERVICE_PLACE = "INPATIENT ACUTE CARE FACILITY" and season.SMALL_SEAS_NUM <> 0
GROUP BY season.SMALL_SEAS_NUM
;
 SMALL_SEAS_NUM | sum(flu.ILI_m) | POPSTAT   | AR100000 |
+----------------+----------------+-----------+----------+
|              1 |           8321 | 274676144 |   3.0293 |
|              2 |          20280 | 283987704 |   7.1411 |
|              3 |          21899 | 286776721 |   7.6362 |
|              4 |          62733 | 290637947 |  21.5845 |
|              5 |          65033 | 292927888 |  22.2010 |
|              6 |          49203 | 295132821 |  16.6714 |
|              7 |          37824 | 298012768 |  12.6920 |
|              8 |          73911 | 300961101 |  24.5583 |
|              9 |          59318 | 304009593 |  19.5118 |
|             10 |         156632 | 306500542 |  51.1033 
/* This metric is okay, and it does not seem to differ substantially from acute care facilities at peak weeks.*/



























