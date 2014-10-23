#evaluation-generator
====================

How to use this script:
Fill out the html form: https://docs.google.com/a/knowlabs.com/forms/d/1aCC1ckzEnd4qF1r6VvWGoiDW9HZuDk44ZN7vglHdgxw/viewform
download the csv that has only the student’s feedback here: https://docs.google.com/a/knowlabs.com/spreadsheets/d/1rBEtBrlEI_6K_MwyGURqvyyRhae8OhnUhv_ypBe-h9g/edit#gid=218712123
place the csv in the same directory as script.
rename the csv to “feedback.csv”
run the script on feedback.csv
this will generate a tex file called evaluation.tex 
run latex on evaluation.tex
you have your evaluation pdf



to dos to refine this script: 

Write code quality items in a “student friendly” format in the html form, e.g. UTF-8 not used -> The project does not use UTF-8 for character encoding.
add version number in the html form
add help text “\par”  \\ for newline in personalmessage field. 
prefilled suggestions for each of the “suggestion fields” in the form. 
download the csv file from the script. 
rename the generated file to incorporate the coursename, version and studentname
give user the ability to choose the student name, so that csv can have more than one student information. 
fix the code so that latex runs without errors. 
write code for exceeds specifications. 
run the latex file through python to generate pdf. 
