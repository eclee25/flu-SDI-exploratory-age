/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 4/6/2013
Function: explore popstat variable

Command Line: mysql -u elizabeth -pbansa11ab mysqltemplate.sql
Data: flu table: SDI
*/

select week, sum(popstat) from flu where agegroup = "TOTAL" and service_place = "TOTAL" and patient_zip3 = "200" group by week;

select week, sum(popstat) from flu where agegroup = "TOTAL" and service_place = "TOTAL" and patient_zip3 = "TOT" group by week;

select week, sum(popstat) from flu where agegroup = "TOTAL" and service_place = "OFFICE/OP CLINICS" and patient_zip3 = "TOT" group by week;

select year(week), sum(popstat) from flu where agegroup = "5-9 YEARS" and service_place = "TOTAL" and patient_zip3 = "TOT" group by year(week);

select year(week), sum(popstat) from flu where agegroup = "5-9 YEARS" and service_place = "TOTAL" and patient_zip3 = "TOT" group by year(week);

select distinct patient_zip3, popstat from flu where popstat = ' ';
-- there were 52 zipcodes that had missing values for at least one row in popstat

-- examine one of these zipcodes
select week, agegroup, patient_zip3, sum(ILI_m), popstat from flu where (agegroup = "5-9 YEARS" or agegroup = "10-14 YEARS") and service_place = "TOTAL" and patient_zip3 = "002" group by week;

select week, agegroup, patient_zip3, ILI_m, popstat from flu where  service_place = "TOTAL" and patient_zip3 = "002" group by week, agegroup;

select week, agegroup, patient_zip3, ILI_m, ANY_DIAG_VISIT_CT from flu where  service_place = "TOTAL" and patient_zip3 = "003" group by week, agegroup;
select week, agegroup, patient_zip3, popstat, ILI_m, ANY_DIAG_VISIT_CT from flu where  service_place = "TOTAL" and patient_zip3 = "311" group by week, agegroup;

-- it seems like there is data missing for whole zipcodes? There are random entries for some weeks and agegroups but very little data exists. Is this because there were no visits in these zipcodes? Perhaps these are very little populated zipcodes. For the data that does exist for these zipcodes, there were very low ILI_m and ANY_DIAG_VISIT_CT numbers

select week, agegroup, patient_zip3, popstat, ILI_m, ANY_DIAG_VISIT_CT from flu where  service_place = "TOTAL" and patient_zip3 = "200" group by week, agegroup;

select week, agegroup, patient_zip3, popstat, ILI_m, ANY_DIAG_VISIT_CT from flu where  service_place = "TOTAL" and patient_zip3 = "963" group by week, agegroup;

-- perhaps popstat doesn't exist if there aren't entries for every type of agegroup and service_place for at least one week 

select week, agegroup, patient_zip3, ILI_m, popstat from flu where  service_place = "TOTAL" and patient_zip3 = (select distinct patient_zip3 from flu where popstat = ' ') 
group by week, agegroup; -- don't know how to make this work


-- 5/31/13 spot check zipcodes with largest popstat values
-- are these the largest urban areas in the US?
select year(week), patient_zip3, popstat from flu
where service_place = "TOTAL" and year(week) = 2010 and agegroup = "TOTAL" and (patient_zip3 = "100" or patient_zip3 = "104" or patient_zip3 = "111" or patient_zip3 = "110" or patient_zip3 = "112" or patient_zip3 = "113")
group by patient_zip3; 
-- some of these NY zipcodes are ~250,000 while Brooklyn and Manhattan are in the >1M and 2M range

select year(week), patient_zip3, popstat from flu
where service_place = "TOTAL" and year(week) = 2010 and agegroup = "TOTAL" and (patient_zip3 = "606")
group by patient_zip3;
-- Chicago is >2M

select year(week), patient_zip3, popstat from flu
where service_place = "TOTAL" and year(week) = 2010 and agegroup = "TOTAL" and popstat > 1500000
group by patient_zip3;

 year(week) | patient_zip3 | popstat   |
+------------+--------------+-----------+
|       2010 | 070          |   1610752 | Newark
|       2010 | 100          |   1566510 | Manhattan
|       2010 | 112          |   2576210 | Brooklyn
|       2010 | 117          |   1585579 | Long Island
|       2010 | 300          |   2289589 | Atlanta
|       2010 | 330          |   1596186 | Southern Florida
|       2010 | 331          |   1862827 | Miami
|       2010 | 600          |   1668149 | Palatine, Chi suburb
|       2010 | 606          |   2830949 | Chicago
|       2010 | 750          |   2103880 | Northern TX
|       2010 | 770          |   3003916 | Houston
|       2010 | 782          |   1558482 | San Antonio
|       2010 | 852          |   1557582 | Phoenix
|       2010 | 900          |   2519426 | Los Angeles
|       2010 | 917          |   2033285 | Industry, LA suburb
|       2010 | 945          |   2272261 | Oakland 

select year(week), patient_zip3, popstat from flu
where service_place = "TOTAL" and year(week) = 2009 and agegroup = "TOTAL" and popstat > 1500000
group by patient_zip3;
-- same zipcodes as in 2010; there is little variation in largest popstat zip3s from 2009 to 2010

-- # 0%: 0.0
-- # 25%: 105,774.5
-- # 50%: 202,375
-- # 75%: 432,941.5
-- # 100%: 3,003,916

-- 6/4/13 spot check zipcodes with smallest popstat values
-- are these rural areas?
select year(week), patient_zip3, popstat from flu
where service_place = "TOTAL" and year(week) = 2010 and agegroup = "TOTAL" and popstat < 30000 and popstat > 0
group by patient_zip3;

 year(week) | patient_zip3 | popstat |
+------------+--------------+---------+
|       2010 | 022          |   26219 | Boston
|       2010 | 036          |   13429 | White Riv Junc (NH/VT)
|       2010 | 051          |   29016 | White Riv Junc (VT)
|       2010 | 059          |    3605 | White Riv Junc (VT)
|       2010 | 102          |   11070 | NYC PO Box/Unique
|       2010 | 369          |   19616 | Meridian, MS pop ~40,000
|       2010 | 414          |   25453 | Campton, KY pop ~424
|       2010 | 516          |   23537 | Shenandoah, IA pop ~5000
|       2010 | 556          |   16095 | North Shore, MN scenic
|       2010 | 576          |   20926 | Mobridge, SD
|       2010 | 588          |   24615 | Williston, ND
|       2010 | 669          |   24903 | Salina, KS
|       2010 | 677          |   29195 | Colby, KS
|       2010 | 679          |   29031 | Liberal, KS
|       2010 | 690          |   24040 | McCook, NE
|       2010 | 692          |    8434 | Valentine, NE
|       2010 | 739          |   28033 | Liberal, OK/KS
|       2010 | 822          |   22896 | Wheatland, WY
|       2010 | 823          |   16452 | Rawlins, WY
|       2010 | 830          |   20185 | Rock Springs, WY
|       2010 | 831          |   20651 | Rock Springs, WY
|       2010 | 878          |   18447 | Socorro, NM
|       2010 | 879          |   17832 | Truth or Conseq, NM
|       2010 | 884          |   15683 | Tucumari, NM
|       2010 | 893          |   10661 | Ely, NV
|       2010 | 994          |   21646 | Lewiston, WA/ID
|       2010 | 999          |   20547 | Ketchikan, AK





















