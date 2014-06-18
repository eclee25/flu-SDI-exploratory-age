#!/usr/bin/python



import csv
#datetime dateutil
#mysql likes dates in year-month-day form

i_f=open('/home/elee/Documents/sdi_rapidd_nolabel.csv','r')
o_f=open('sdi_rapidd_clean_9_12_12.csv', 'wb')
infile=csv.reader(i_f, delimiter=',')
outfile=csv.writer(o_f, delimiter=',')
ct=0
for row in infile:
	d = row[0].split('/')
	if row[0] == 'SVC_WEEK':
		headers=['SVC_WEEK', 'PATIENT_ZIP3', 'AGEGROUP', 'SERVICE_PLACE', 'ILI_m', 'RSV_m', 'POPSTAT', 'ANY_DIAG_VISIT_CT', 'WEEK']
		outfile.writerow(headers)
		continue
	elif len(d[0])==1 and len(d[1])==1:
		a=d[2]+'-0'+d[0]+'-0'+d[1]
	elif len(d[0])==1 and len(d[1])==2:
		a=d[2]+'-0'+d[0]+'-'+d[1]
	elif len(d[0])==2 and len(d[1])==1:
		a=d[2]+'-'+d[0]+'-0'+d[1]
	elif len(d[0])==2 and len(d[1])==2:
		a=d[2]+'-'+d[0]+'-'+d[1]
	else:
		print row
		break
	newrow=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],a]
	outfile.writerow(newrow)
	ct+=1
print ct	

i_f.close()
o_f.close()


