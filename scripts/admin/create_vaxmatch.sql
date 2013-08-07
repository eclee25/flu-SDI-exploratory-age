/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 5/21/13
Function: Create table that shows vaccine match data, where vaccine match is defined through  

antigenic similarity, minor antigenic variant that confers reduced titers to ferret antisera produced against the vaccine strain, or other cross-reactivity confer a match between a circulating and vaccine strain

redundant information with subtype table (calculates percentages from that data)

Command Line: mysql -u elizabeth -pbansa11ab <create_vaxmatch.sql

Data: 
(subtype data)
2000-2007 seasons from source http://www.cdc.gov/mmwr/preview/mmwrhtml/mm5933a1.htm
There are differences between the prominent subtypes identified in this document and the percentage of H1, H3, and B isolates that are found in the Flu Season Summaries. 8/7/13 ECL

CDC Flu Season Summary 2007-08, CDC Flu Season Summary 2008-09, CDC Flu Season Summary 2009-10 from source http://www.cdc.gov/flu/weekly/pastreports.htm
(vaxmatch data)
CDC Flu Season Summaries for each season from 2000-10 from http://www.cdc.gov/flu/weekly/pastreports.htm

See USfluvaxdata_June13.ods spreadsheet


Codebook:
SUBTYPE_marker: 1 = H1; 2 = H3; 3 = B; 4 = H1 & H3; 5 = H1 & B; 6 = H3 & B; 7 = H1 & H3 & B
H1_MATCH: percent of H1 virus isolates that were characterized as antigenically similar to the H1 component of the season's Northern Hemisphere trivalent flu vaccine, rounded to the nearest whole percent. 
H3_MATCH: same as H1_MATCH with H3 virus isolates
B_MATCH: same as H1_MATCH with B virus isolates across both Yamagata and Victoria lineages. M
TOT_MATCH: percent of all virus isolates that were characterized as antigenically similar to any of the trivalent vaccine strains, rounded to the nearest whole percent. These levels are not the same to those used by the CDC website to categorize vaccine strain match.
MLVL: qualitative code that represents level of vaccine strain match with strains circulating during the season. This is calculated as percent of virus isolates that match one vaccine strain in the trivalent vaccine out of the total number of virus isolates collected that season. These are the codes we have defined: very low = 0-20%; low = 21-40%; medium = 41-60%; high = 61-80%; very high = 81-100%
MLVL_marker: match level marker for plotting 1 = very low; 2 = low; 3 = medium; 4 = high; 5 = very high

8/7/13: reimported vaxmatch table into database with corrected prominent subtypes
*/

USE sdi;
DROP TABLE if exists vaxmatch;

CREATE TABLE vaxmatch (
	SEASON_NUM INT(2),
	SEASON_YRS VARCHAR(5),
	SUBTYPE VARCHAR(12),
	SUBTYPE_marker INT(1),
	H1_MATCH INT(3),
	H3_MATCH INT(3),
	B_MATCH INT(3),
	TOT_MATCH INT(3),
	MLVL VARCHAR(10),
	MLVL_marker INT(1)
);	

INSERT INTO vaxmatch
VALUES 
(1,'00-01','H1 & B',5,100,100,100,100,'very high',5),
(2,'01-02','H3 & B',6,100,100,23,70,'high',4), /*H1N2 isolate had antigenically similar H1 protein to vax strain; minor antigenic B variants*/
(3,'02-03','H1 & H3 & B',7,100,100,100,100,'very high',5), /*H1N2 isolate had antigenically similar H1 protein to vax strain*/
(4,'03-04','H3',2,100,11,7,11,'very low',1), /*similar HA*/
(5,'04-05','H3 & B',6,100,22,74,40,'low',2), /*similar HA*/
(6,'05-06','H3 & B',6,100,100,19,74,'high',4),
(7,'06-07','H1 & H3 & B',7,100,100,77,93,'very high',4),
(8,'07-08','H1 & H3 & B',7,66,23,2,32,'low',2),
(9,'08-09','H1 & B',5,100,100,17,77,'high',4),
(10,'09-10','H1',1,100,100,88,99,'very high',5) /* H1_MATCH includes both strain match to 2009 pH1N1 monovalent vaccine and seasonal strain to trivalent vaccine)*/
;






















