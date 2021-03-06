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







