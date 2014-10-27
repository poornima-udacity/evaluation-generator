import csv
import shutil
import pprint
import re
import sys
import gspread
import getpass
import os


#_criteria dicts define the statement to put in the evaluation for wheather or not a student meets specification on a criteria.
design_criteria = {"design1" : ("The DOM tree correctly represents the page content.", 
	"The DOM tree does not represent the page content."),
 "design2" : ("Page elements use semantic tags where appropriate.", 
 	"Page elements do not appropriately use semantic tags."), 
 "design3" : ("Design uses grid based layout principles.", 
 	"Design does not use grid based layout principles.")}

responsive_criteria = {"responsive1" : ("Portfolio is responsively designed.", 
	"Portfolio is not responsively designed."),
	"responsive2" : ("Portfolio renders appropriately." , "Portfolio does not render appropriately."),
	"responsive3" : ("Portfolio includes all required components on all three required devices [iPad, Nexus 5 Phone, and laptop].",  
		"Portfolio does not include all required components on all three required devices [iPad, Nexus 5 Phone, and laptop].")}

separationofconcerns_criteria = {"separationofconcerns1" : ("Portfolio completely separates structure (HTML) from design/style (CSS).", 
	"Portfolio does not completely separate structure (HTML) from design/style (CSS).")}

codequality_criteria = {"codequality1" : ("Code is formatted with consistent, logical, and easy-to-read formatting as described in the Udacity HTML/CSS style guide.", 
	"Code does not follow the format specified in the Udacity HTML/CSS style guide.")}

#all the sections and associated criteria directories. 
section_criteria = {"design" : design_criteria, "responsive" : responsive_criteria, "separationofconcerns" : separationofconcerns_criteria, "codequality" : codequality_criteria }

#this code is to ensure the list formatting of observations and suggestions. Observation and suggestion list will show up only in the case when a criteria is not met
for criteria in section_criteria:
	#print type(criteria), type(section_criteria[criteria])
	for key in section_criteria[criteria]:
		#print section_criteria[criteria][key][1]
		section_criteria[criteria][key] = (section_criteria[criteria][key][0],
			section_criteria[criteria][key][1] + "\\begin{itemize} *"  + key + "observation* *" + key + "suggestion* \end{itemize}")



def get_evaluation_dict(studentname, version):
	""" call the google server and get the student evaluation from the form csv. return a dictionary 
	of the evaluation response from the csv file. 
	"""
	spreadsheet = google_login.open_by_key('1kg7BzshWQx3AL4QU13uPrkPxtzY7fY55RYtRIsOSenI').sheet1
	header = spreadsheet.row_values(1)
	version_index = header.index('version')
	cell_list = spreadsheet.findall(studentname)
	evaluation_dict = {}
	for cell in cell_list:
		if int(spreadsheet.row_values(cell.row)[version_index]) == int(version):
			student_performance = spreadsheet.row_values(cell.row)
			evaluation_dict = dict(zip(header, student_performance))

	if evaluation_dict == {}:
		return "student does not exist"

	return evaluation_dict


#this function creates a dict with yes and nos depending on whether the student satisfies a criteria from design.
#function also creates separate dictionaries for observations and suggestions. 
def get_section_dict(evaluation_dict, section_name):
	""" separate the evaluation for each section from the section dictionary. This will create a separate observation
	and suggestion dictionary.
	"""
	section_dict = {k:v for (k,v) in evaluation_dict.iteritems() if (section_name in k and k[-1].isdigit()) }
	observations_dict = {k:v for (k,v) in evaluation_dict.iteritems() if ("observation" in k and section_name in k) }
	suggestions_dict = {k:v for (k,v) in evaluation_dict.iteritems() if ("suggestion" in k and section_name in k ) }

	if section_name == "codequality":
		observations_dict["codequality1observation"] =  "".join(evaluation_dict["codequality1"].split(",")).strip()
		suggestions_dict["codequality1suggestion"] = evaluation_dict["codequality1suggestion"]

	if section_name == "studentinfo":
		section_dict["studentname"] = evaluation_dict["studentname"]
		section_dict["personalmessage"] = evaluation_dict["personalmessage"]

	return section_dict, observations_dict, suggestions_dict

#to get student name and personal message. 
def get_student_info(evaluation_dict):
	""" returns the dictionary of student specific information - name, personalmessage and project version. 
	"""
	student_info = {}
	student_info["studentname"] =  evaluation_dict["studentname"]
	student_info["personalmessage"] =  evaluation_dict["personalmessage"]
	student_info["version"] = evaluation_dict["version"]
	return student_info


#this function creates appropriate statements for inserting in evaluation. 
def get_section_evaluation(evaluation_dict, section_name):
	""" create a dictionary of the evaluation for the given section in a format that can be directly inserted in 
	the tex file. 
	"""
	section_dict, observations_dict, suggestions_dict = get_section_dict(evaluation_dict, section_name)
	section_evaluation = {}
	section_conclusion = section_name + "conclusion"
	section_evaluation[section_conclusion] = "Meets Specifications"
	#section_criteria is the one that describes in words whether or not a criteria meets specifications in that section. 
	for key in section_dict:
		if section_dict[key] == "Yes":
			section_evaluation[key] = section_criteria[section_name][key][0]

		else:
			section_evaluation[key] = section_criteria[section_name][key][1]
			observation = ''
			suggestion = ''

			if suggestions_dict[key+ 'suggestion']:
				suggestion = "\item \\textcolor{caputmortuum}{" + suggestions_dict[key+ 'suggestion']   + "}"
			
			if observations_dict[key+ 'observation']:
				observation = "\item \\textcolor{darkolivegreen}{" + observations_dict[key+ 'observation'] + "}"

			section_evaluation[key] = section_evaluation[key].replace("*" + key + "suggestion*", suggestion)
			section_evaluation[key] = section_evaluation[key].replace("*" + key + "observation*", observation)
			
			section_evaluation[section_conclusion] = "Does Not Meet Specifications"
	return section_evaluation

#creating a dictionary of all appropriate statements and placeholders. 
def get_all_evaluation(evaluation_dict):
	""" loop over all the sections and creates the appropriate text for all the sections to be inserted in tex.
	"""
	all_evaluation = {}
	section_names = ['design', 'responsive', 'separationofconcerns', 'codequality']
	for section in section_names:
		all_evaluation.update(get_section_evaluation(evaluation_dict, section))

	all_evaluation.update(get_student_info(evaluation_dict))
	all_evaluation["projectconclusion"] = "Project Meets Specifications"
	for section in section_names:
		if all_evaluation[section+'conclusion'] == "Does Not Meet Specifications":
			all_evaluation["projectconclusion"] = "Project Does Not Meet Specifications"

	return all_evaluation

#inserts the evaluation into the latex file. 
def insert_into_latex(evaluation_dict):
	""" inserting the evaluation dictionary in the appropriate placeholders.
	"""
	all_evaluation = get_all_evaluation(evaluation_dict)
	template = open("evaluation_template.tex", 'r')
	evaluation_file_name = "Mockup To Website - Project Evaluation v" + all_evaluation["version"] + " - " + all_evaluation['studentname'] + ".tex"
	generated_evaluation = open(evaluation_file_name, 'w')
	for line in template:
		for key, value in all_evaluation.iteritems():
			if value: 
				value = value.strip()
			else:
				value = ''
			if value in ["\item \\textcolor{darkolivegreen}{" + "}", "\item \\textcolor{caputmortuum}{" + "}"]:
				value = ''
			line = line.replace('*' + key + '*', value)
		generated_evaluation.write(line)
	generated_evaluation.close()
	template.close()
	evaluation_file_name = "\ ".join(evaluation_file_name.split(" "))
	os.system("pdflatex " + evaluation_file_name)
	#following code deletes the generated files. 
	aux_files= [evaluation_file_name[:-3] + "aux", evaluation_file_name[:-3] + "log"]
	for aux in aux_files:
		os.system("rm " + aux)



if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: process_csv_create_latex.py <studentname> <version>"
	else: 
		studentname, version = sys.argv[1:] 
		username = input("enter your knowlabs email: ")
		password = getpass.getpass('Enter your knowlabs password: ')
		google_login = gspread.login(username, password)    	
		evaluation_dict =  get_evaluation_dict(studentname, int(version))
    	#print evaluation_dict, type(evaluation_dict)
    	insert_into_latex(evaluation_dict)

    	

    	





