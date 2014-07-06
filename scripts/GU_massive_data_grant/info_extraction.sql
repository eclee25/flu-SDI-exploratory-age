
-- Could you also tell me (approx) how many raw cases are reported in a single week at the peak of a flu outbreak in the SDI data, and what the raw numbers for total number of cases per season is.



select WEEK, max(ILI_m) from flu 
WHERE SERVICE_PLACE = 'TOTAL' and AGEGROUP = 'TOTAL' and PATIENT_ZIP3 = 'TOT'
GROUP BY WEEK;
-- 42k, 50k, 65k, 41k, 126k, 76k, 84k, 183k, 125k, 375K

select season.season_num, sum(flu.ILI_m) from flu right join season on (flu.week = season.week)
WHERE flu.SERVICE_PLACE = 'TOTAL' and flu.AGEGROUP = 'TOTAL' and flu.PATIENT_ZIP3 = 'TOT'
GROUP by season.season_num
;
-- 1.1M to 4.9M