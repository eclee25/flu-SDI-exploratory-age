USE sdi;
DROP TABLE if exists flu;

CREATE TABLE flu (
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	WEEK DATE,
	PATIENT_ZIP3 VARCHAR(3),
	AGEGROUP VARCHAR(12),
	SERVICE_PLACE VARCHAR(30),
	ILI_m INT,
	RSV_m INT,
	POPSTAT INT,
	ANY_DIAG_VISIT_CT INT
);	
	
LOAD DATA LOCAL INFILE '/home/elee/Documents/sdi_rapidd_clean_9_12_12.csv' INTO TABLE flu
FIELDS TERMINATED BY ','
IGNORE 1 LINES
(@dummy, PATIENT_ZIP3, AGEGROUP, SERVICE_PLACE, ILI_m, RSV_m, POPSTAT, ANY_DIAG_VISIT_CT, WEEK)
;
