/*----SQL TEMPLATE----
Author: Elizabeth Lee
Date: 5/20/13
Function: Create table subtype that lists the prominent flu subtypes for each season of the dataset. Prominent subtype is defined as at least 20% of all isolates that were typed or subtyped in that season.

Command Line: mysql -u elizabeth -pbansa11ab <create_subtype.sql

Data: 2000-2007 seasons from source http://www.cdc.gov/mmwr/preview/mmwrhtml/mm5933a1.htm; There are differences between the prominent subtypes identified in this document and the percentage of H1, H3, and B isolates that are found in the Flu Season Summaries. 8/7/13 ECL
CDC Flu Season Summary 2007-08, CDC Flu Season Summary 2008-09, CDC Flu Season Summary 2009-10 from source http://www.cdc.gov/flu/weekly/pastreports.htm
See USfluvaxdata_June13.ods spreadsheet

Codebook:
SUBTYPE: prominent subtype(s) for that season
SUBTYPE_marker: 1 = H1; 2 = H3; 3 = B; 4 = H1 & H3; 5 = H1 & B; 6 = H3 & B; 7 = H1 & H3 & B
(H1, H3, B, TOT)_ISOLATES: Number of isolates collected that season
(H1, H3, B, TOT)_MATCH Number of isolates collected that season that match the vaccine strains (H1, H3, B, trivalent vax in general)

8/7/13: reimported subtype table into database with corrected prominent subtypes
*/


USE sdi;
DROP TABLE if exists subtype;

CREATE TABLE subtype (
	SEASON_NUM INT(2),
	SEASON_YRS VARCHAR(5),
	SUBTYPE VARCHAR(12),
	SUBTYPE_marker INT(1),
	H1_ISOLATES INT(4),
	H3_ISOLATES INT(4),
	B_ISOLATES INT(4),
	TOT_ISOLATES INT(4),
	H1_MATCH INT(4),
	H3_MATCH INT(4),
	B_MATCH INT(4),
	TOT_MATCH INT(4)
);	

INSERT INTO subtype
VALUES 
(1,'00-01','H1 & B',5, 354, 23, 301, 678, 354, 23, 301, 678),
(2,'01-02','H3 & B',6, 30, 393, 267, 690, 30, 393, 61, 484),
(3,'02-03','H1 & H3 & B',7, 287, 143, 269, 699, 287, 143, 268, 698),
(4,'03-04','H3',2, 3, 949, 71, 1024, 3, 106, 5, 114),
(5,'04-05','H3 & B',6, 11, 709, 355, 1075, 11, 156, 264, 431),
(6,'05-06','H3 & B',6, 135, 563, 321, 1019, 135, 563, 60, 758),
(7,'06-07','H1 & H3 & B',7, 486, 289, 332, 1107, 486, 289, 254, 1029),
(8,'07-08','H1 & H3 & B',7, 407, 404, 350, 1161, 270, 91, 6, 367),
(9,'08-09','H1 & B',5, 723, 107, 307, 1137, 723, 107, 51, 881),
(10,'09-10','H1',1, 1906, 14, 43, 1963, 1897, 14, 38, 1949)
;

