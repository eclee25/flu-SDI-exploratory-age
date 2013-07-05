USE sdi;
DROP TABLE if exists child;

CREATE TABLE child (
	AGEGROUP VARCHAR(12),
	MARKER VARCHAR(2)
);	

INSERT INTO child
VALUES 
('<2 YEARS','O'),
 ('2-4 YEARS','O'),
 ('5-9 YEARS','C'),
 ('10-14 YEARS','C'),
 ('15-19 YEARS','C'),
 ('20-29 YEARS','A'),
 ('30-39 YEARS','A'),
 ('40-49 YEARS','A'),
 ('50-59 YEARS','A'),
 ('60-69 YEARS','O'),
 ('70-79 YEARS','O'),
 ('80+ YEARS','O');
