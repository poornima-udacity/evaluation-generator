import csv
import shutil
import pprint
import re


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
	print type(criteria), type(section_criteria[criteria])
	for key in section_criteria[criteria]:
		print section_criteria[criteria][key][1]
		section_criteria[criteria][key] = (section_criteria[criteria][key][0],
			section_criteria[criteria][key][1] + "\\begin{itemize} *"  + key + "observation* *" + key + "suggestion* \end{itemize}")

#this function creates a dict with yes and nos depending on whether the student satisfies a component from design.
def get_section_dict(section_name):
	with open('feedback.csv', 'rb') as csvfile:
		feedbackreader = csv.reader(csvfile)
		all_criteria = feedbackreader.next()
		all_criteria = [x.strip() for x in all_criteria]
		student_performance = feedbackreader.next()

		evaluation_dict = dict(zip(all_criteria, student_performance))
		#print "evaluation_dict", evaluation_dict
	section_dict = {k:v for (k,v) in evaluation_dict.iteritems() if (section_name in k and k[-1].isdigit()) }
	observations_dict = {k:v for (k,v) in evaluation_dict.iteritems() if ("observation" in k and section_name in k) }
	suggestions_dict = {k:v for (k,v) in evaluation_dict.iteritems() if ("suggestion" in k and section_name in k ) }

	if section_name == "codequality":
		observations_dict["codequality1observation"] =  evaluation_dict["codequality1"].strip()
		suggestions_dict["codequality1suggestion"] = ""

	if section_name == "studentinfo":
		section_dict["studentname"] = evaluation_dict["studentname"]
		section_dict["personalmessage"] = evaluation_dict["personalmessage"]


	#responsiveness_dict = {k:v for (k,v) in evaluation_dict.iteritems() if "responsiveness" in k}
	#print "design dict", design_dict
	#print evaluation_dict
	return section_dict, observations_dict, suggestions_dict

def get_student_info():
	student_info = {}
	with open('feedback.csv', 'rb') as csvfile:
		feedbackreader = csv.reader(csvfile)
		all_criteria = feedbackreader.next()
		all_criteria = [x.strip() for x in all_criteria]
		student_performance = feedbackreader.next()
		evaluation_dict = dict(zip(all_criteria, student_performance))
	student_info["studentname"] =  evaluation_dict["studentname"]
	student_info["personalmessage"] =  evaluation_dict["personalmessage"]
	return student_info


#this function creates appropriate statements for inserting in evaluation. 
def get_section_evaluation(section_name):
	section_dict, observations_dict, suggestions_dict = get_section_dict(section_name)

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


def get_all_evaluation():
	all_evaluation = {}
	section_names = ['design', 'responsive', 'separationofconcerns', 'codequality']
	for section in section_names:
		all_evaluation.update(get_section_evaluation(section))

	all_evaluation.update(get_student_info())
	all_evaluation["projectconclusion"] = "Project Meets Specifications"
	for section in section_names:
		if all_evaluation[section+'conclusion'] == "Does Not Meet Specifications":
			all_evaluation["projectconclusion"] = "Project Does Not Meet Specifications"

	return all_evaluation


def insert_into_latex():
	all_evaluation = get_all_evaluation()
	template = open("evaluation_template.tex", 'r')

	generated_evaluation = open("evaluation.tex", 'w')

	for line in template:
		for key, value in all_evaluation.iteritems():
			if value.strip() in ["\item \\textcolor{darkolivegreen}{" + "}", "\item \\textcolor{caputmortuum}{" + "}"]:
				value = ''
			line = line.replace('*' + key + '*', value)
		generated_evaluation.write(line)
	generated_evaluation.close()
	template.close()

insert_into_latex()





