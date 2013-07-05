--September 2012, SDI data
--do not run this file as script

----------------------------------------------------
----characterizing the data----
--there is only one week's worth of 2000 data
--data is collected weekly
--AGEGROUP, SERVICE_PLACE, and PATIENT_ZIP3 have "total" categories that need to be utilized in order to capture the entirety of the data (active specification needed if no filtering on one of these three variables)

--explore 2000 data--
SELECT WEEK, ILI_m, ANY_DIAG_VISIT_CT, AGEGROUP from flu
WHERE (YEAR(WEEK) = 2010)
GROUP BY WEEK, AGEGROUP
;--2000 data only exists for the last week in 2000. this would explain the small numbers. 2010 data exists through end of June. Considering the truncation for this year, 2010 had a high number of ILI cases and total number of visits.
--the sums for ILI_m and ANY_DIAG_VISIT_CT for each AGEGROUP per WEEK do not sum add up to the total values for "TOTAL" in AGEGROUP. The values are smaller. **NOTE: Need to specify "TOTAL" for each categorical variable (ie. agegroup, service_place, patient_zip3)
---------------------

--average number of ILI diagnoses per year
SELECT YEAR(WEEK), avg(ILI_m) from flu
WHERE AGEGROUP = "TOTAL" AND SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3 = "TOT"
GROUP BY YEAR(WEEK)
;--the average number of ILI diagnoses was heightened in the 2008-2010 time period with a dramatic peak in 2009

--average number of visits per year
SELECT YEAR(WEEK), avg(ANY_DIAG_VISIT_CT) from flu
WHERE AGEGROUP = "TOTAL" AND SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3 = "TOT"
GROUP BY YEAR(WEEK)
;--the average number of visits per year has increased over time

--agegroup and ILI as a proportion of all visits
SELECT AGEGROUP, YEAR(WEEK), sum(ILI_m), sum(ANY_DIAG_VISIT_CT), sum(ILI_m)/sum(ANY_DIAG_VISIT_CT) as ILI_prop FROM flu
WHERE SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3 = "TOT"
GROUP BY AGEGROUP, YEAR(WEEK)
;--trends: ages under 10 had the greatest proportion of ILI among all visits across all years; 
--at older ages (>=60) there was little variation in proportion of ILI among all visits across all 10 years (exclude 2001); 
--at ages below 60, there was a small spike in 2003 and a large spike in 2009 in ILI proportion. consequently, these spikes are observed as well in the total population;

--for children under 10, ILI as a proportion of visits in each service place
SELECT AGEGROUP, YEAR(WEEK), SERVICE_PLACE, sum(ILI_m), sum(ANY_DIAG_VISIT_CT), sum(ILI_m)/sum(ANY_DIAG_VISIT_CT) as ILI_prop FROM flu
WHERE (AGEGROUP = "<2 YEARS" OR AGEGROUP = "2-4 YEARS" OR AGEGROUP = "5-9 YEARS") AND PATIENT_ZIP3 = "TOT" AND YEAR(WEEK) != 2000
GROUP BY AGEGROUP, SERVICE_PLACE, YEAR(WEEK)
;--trends: for children under 10, office/OP clinics receive the most visits but the greatest ILI proportion was at emergency/urgent care; 
--2009 saw noticeable spikes in ILI proportion, most dramatically in emergency/urgent care and inpatient acute care

--what are the seasonal variations in ILI reporting? chose five years that did not have large non-seasonal epidemics
SELECT WEEK, ILI_m, ILI_m/ANY_DIAG_VISIT_CT from flu
WHERE AGEGROUP = "TOTAL" AND SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3 = "TOT" AND (YEAR(WEEK) = 2003 OR YEAR(WEEK)=2004 OR YEAR(WEEK)=2005 OR YEAR(WEEK)=2006 OR YEAR(WEEK)=2007)
GROUP BY WEEK
;--ILI diagnosis peaks occur approximately once a year (in terms of counts and proportion of visits) for a period of 4-8 consecutive weeks. They occur during the winter months -- starting in November for some years and as late as February in other years. These peaks consisted of at least 1% of all diagnoses being ILI for that week.

------zipcode module-------
--filter most affected zipcodes by looking at incidence across all years
SELECT sum(ILI_m), PATIENT_ZIP3 from flu
WHERE AGEGROUP = "TOTAL" AND SERVICE_PLACE = "TOTAL"
GROUP BY PATIENT_ZIP3
ORDER BY sum(ILI_m) DESC
; --grab 10 highest ILI incident zipcodes over entire period and the 5 lowest (330, 331, 750, 334, 300, 112, 070, 770, 117, 760) (509, 569, 889, 842, 649). it might be interesting to see if the incidents in the least affected zips occurred during the most affected time periods of the most affected zips
---check--- a few zipcodes and sums from previous table
SELECT sum(ILI_m), PATIENT_ZIP3, YEAR(WEEK) from flu
WHERE AGEGROUP = "TOTAL" AND SERVICE_PLACE = "TOTAL" AND PATIENT_ZIP3 = "998"
GROUP BY PATIENT_ZIP3, YEAR(WEEK)
;--sums are correct
--table of the 10 chosen zipcodes by year to see consistency across years
SELECT sum(ILI_m), PATIENT_ZIP3, YEAR(WEEK) from flu
WHERE (PATIENT_ZIP3 = 330 or PATIENT_ZIP3 = 331 or PATIENT_ZIP3 = 750 or PATIENT_ZIP3 = 334 or PATIENT_ZIP3 = 300 or PATIENT_ZIP3 = 112 or PATIENT_ZIP3 = 070 or PATIENT_ZIP3 = 770 or PATIENT_ZIP3 = 117 or PATIENT_ZIP3 =760) AND (AGEGROUP = "TOTAL" AND SERVICE_PLACE = "TOTAL" AND YEAR(WEEK) != 2000)
GROUP BY PATIENT_ZIP3, YEAR(WEEK)
;--do these zips track with the top 10 most ILI-incident zipcodes in 2009?
SELECT sum(ILI_m), PATIENT_ZIP3 from flu
WHERE AGEGROUP = "TOTAL" AND SERVICE_PLACE = "TOTAL" AND YEAR(WEEK)=2009
GROUP BY PATIENT_ZIP3, YEAR(WEEK)
ORDER BY sum(ILI_m)
;--top 10 (112, 750, 331, 330, 070, 117, 300, 334, 913, 917) 770 and 760 had high incidence outside of 2009, 913 and 917 had unusually high incidence in 2009; narrow the high incidence zipcodes to these 4 cases (770, 760, 913, 917)
SELECT ILI_m, ILI_m/ANY_DIAG_VISIT_CT, PATIENT_ZIP3, WEEK from flu
WHERE PATIENT_ZIP3 = 770 AND (AGEGROUP = "TOTAL" AND SERVICE_PLACE = "TOTAL" AND YEAR(WEEK) != 2000)
GROUP BY WEEK
; --ILI proportion was consistently above 1% for all months of the year from 2001 through mid 2006. After that time, seasonal ILI peaks reached 1-2% of visits at approximately 1 year periods. It was unusual that two peaks occurred in 2009 - one in Jan-Feb and one longer one from Sept through Nov.
SELECT ILI_m, PATIENT_ZIP3, WEEK from flu
WHERE PATIENT_ZIP3 = 760 AND (AGEGROUP = "TOTAL" AND SERVICE_PLACE = "TOTAL" AND YEAR(WEEK) != 2000)
GROUP BY WEEK
; --exported in testexport.sql to testexport.csv
SELECT ILI_m, PATIENT_ZIP3, WEEK from flu
WHERE PATIENT_ZIP3 = 913 AND (AGEGROUP = "TOTAL" AND SERVICE_PLACE = "TOTAL" AND YEAR(WEEK) != 2000)
GROUP BY WEEK
;
SELECT ILI_m, PATIENT_ZIP3, WEEK from flu
WHERE PATIENT_ZIP3 = 917 AND (AGEGROUP = "TOTAL" AND SERVICE_PLACE = "TOTAL" AND YEAR(WEEK) != 2000)
GROUP BY WEEK
;

-----------------------------

--------------------wip--------------------
--average per age group of visits for all years
SELECT AGEGROUP, avg(vpy)) as avg_visits FROM flu, (SELECT AGEGROUP, YEAR(WEEK), sum(ANY_DIAG_VISIT_CT) as vpy FROM flu WHERE SERVICE_PLACE = "TOTAL" GROUP BY AGEGROUP,YEAR(WEEK))
WHERE vpy = 
GROUP BY AGEGROUP
;
--average per age group of ILI reports for all years



--how to subset on derived variable ILI_prop?
--work on output
--examine one zipcode: 

