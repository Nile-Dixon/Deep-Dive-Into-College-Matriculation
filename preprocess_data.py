import pandas as pd 


ap_export = []
demographic_export = {'2015':{},'2016':{},'2017':{},'2018':{}}
matriculation_export = {'2015':{},'2016':{},'2017':{},'2018':{}}
sat_export = []
school_type_export = []
spec_pop_export = []

years = ['2015','2016','2017','2018']

print('FORMATTING AP DATA')
#PROCESS AP DATA
for year in years:
	ap_df = pd.read_csv('data/ap/{}.csv'.format(year))
	all_student_rows = ap_df[ap_df['Group'] == 'All Students']
	for index, row in all_student_rows.iterrows():
		ap_export.append([year, row['Campus'], row['CampName'], row['District'], row['Part_Rate']])

print('FORMATTING DEMOGRAPHIC DATA')
#PROCESS DEMOGRAPHIC DATA
for year in years:
	demo_df = pd.read_csv('data/demographics/{}.csv'.format(year))
	#all_student_rows = demo_df[demo_df]
	for index, row in demo_df.iterrows():
		if row['Campus Number'] not in demographic_export[year]:
			demographic_export[year][row['Campus Number']] = {}
		demographic_export[year][row['Campus Number']][row['Ethnicity Name']] = max(4,row['Enrollment by Ethnicity'])

print('FORMATTING MATRICULATION DATA')
#PROCESS MATRICULATION DATA
for year in years:
	matriculation_df = pd.read_csv('data/matriculation/{}.csv'.format(year))
	for index, row in matriculation_df.iterrows():
		if row['Code'] not in matriculation_export[year]:
			matriculation_export[year][row['Code']] = {}
		if row['Institution'] in ['Not found ','Total high school graduates ','Not trackable ']:
			matriculation_export[year][row['Code']][row['Institution']] = row['Students']

print('FORMATTING SAT DATA')
#PROCESS SAT DATA
for year in years:
	sat_df = pd.read_csv('data/sat/{}.csv'.format(year))
	all_student_rows = sat_df[sat_df['Group'] == 'All Students']
	for index, row in all_student_rows.iterrows():
		if year in ['2015','2016']:
			sat_export.append([year, row['Campus'], row['CampName'], row['District'], row['Part_Rate'], row['Math'], row['Reading']])
		else:
			sat_export.append([year, row['Campus'], row['CampName'], row['District'], row['Part_Rate'], row['Math'], row['ERW']])

print('FORMATTING SCHOOL DATA')
#PROCESS SCHOOL TYPE DATA
for year in years:
	school_type_df = pd.read_csv('data/school_type/{}.csv'.format(year))
	for index, row in school_type_df.iterrows():
		if year == '2018':
			school_type_export.append([year, row['District Number'], row['TEA Description']])
		else:
			school_type_export.append([year, row['District'], row['Description']])


print('FORMATTING SPECIAL POPS')
#PROCESSING SPECIAL POPULATION DATA
for year in years:
	specpop_df = pd.read_csv('data/specpops/{}.csv'.format(year))
	for index, row in specpop_df.iterrows():
		spec_pop_export.append([
			year, 
			row['DISTRICT NUMBER'],
			row['CAMPUS NUMBER'],
			row['TOTAL ENROLLMENT'],
			max(row['TOTAL G & T STUDENTS'],4),
			max(row['TOTAL CTE STUDENTS'],4),
			max(row['TOTAL LEP STUDENTS'],4),
			max(row['TOTAL BILINGUAL STUDENTS'],4),
			max(row['TOTAL ESL STUDENTS'],4),
			max(row['TOTAL ECONOMICALLY DISADVANTAGED STUDENTS'],4),
			max(row['TOTAL STUDENTS RECEIVING SPECIAL EDUCATION SERVICES'],4)
		])

print('SAVING AP DATA')
ap_df = pd.DataFrame(data = ap_export, 
	columns = ['YEAR','CAMPUS ID','CAMPUS NAME','DISTRICT ID','AP PARTICIPATION RATE'])
ap_df.to_csv('data/ap_data.csv', index = False)


print('SAVING DEMOGRAPHIC DATA')
demographic_rows = []
for year in demographic_export.keys():
	for campus in demographic_export[year].keys():
		demographic_rows.append([
			year,
			campus,
			demographic_export[year][campus].get('Asian',0),
			demographic_export[year][campus].get('American Indian or Alaska Native',0),
			demographic_export[year][campus].get('Black or African American',0),
			demographic_export[year][campus].get('Hispanic',0),
			demographic_export[year][campus].get('Native Hawaiian/Other or Pacific Islander',0),
			demographic_export[year][campus].get('Two or More Races',0),
			demographic_export[year][campus].get('White',0)
		])
demographic_df = pd.DataFrame(data = demographic_rows, 
	columns = ['YEAR','CAMPUS ID','ASIAN','NATIVE AMERICAN','BLACK','HISPANIC','HAWAIIAN','TWO RACES','WHITE'])
demographic_df.to_csv('data/demographic_data.csv', index = False)

print('SAVING MATRICULATION DATA')
matriculation_rows = []
for year in matriculation_export.keys():
	for campus in matriculation_export[year].keys():
		matriculation_rows.append([
			year,
			campus,
			matriculation_export[year][campus].get('Total high school graduates ',0),
			matriculation_export[year][campus].get('Not found ',0),
			matriculation_export[year][campus].get('Not trackable ',0)
		])
matriculation_df = pd.DataFrame(data = matriculation_rows, 
	columns = ['YEAR','CAMPUS ID','HIGH SCHOOL STUDENTS','NOT FOUND','NOT TRACKABLE'])
matriculation_df.to_csv('data/matriculation_data.csv', index = False)

print('SAVING SAT DATA')
sat_df = pd.DataFrame(data = sat_export, 
	columns = ['YEAR','CAMPUS ID','CAMPUS NAME','DISTRICT ID','SAT PARTICIPATION RATE','SAT MATH','SAT ERW'])
sat_df.to_csv('data/sat_data.csv', index = False)

print('SAVING SCHOOL TYPE DATA')
school_type_df = pd.DataFrame(data = school_type_export, 
	columns = ['YEAR','DISTRICT ID','DESCRIPTION'])
school_type_df.to_csv('data/school_type_data.csv', index = False)

print('SAVING SPECIAL POPS DATA')
special_pops_df = pd.DataFrame(data = spec_pop_export, 
	columns = ['YEAR','DISTRICT ID','CAMPUS ID','ENROLLMENT','GT','CTE','LEP','BIL','ESL','DISADV','SPED'])
special_pops_df.to_csv('data/special_pops_data.csv', index = False)

print('FINISHED')