#evaluation-generator
====================
### generates latex for the evaluation based on the form responses. 

##system requirements
latex! 

##How to use this script:
1. Fill out the html form: https://docs.google.com/a/knowlabs.com/forms/d/1aCC1ckzEnd4qF1r6VvWGoiDW9HZuDk44ZN7vglHdgxw/viewform
2. download the csv that has only the student’s feedback here: https://docs.google.com/a/knowlabs.com/spreadsheets/d/1rBEtBrlEI_6K_MwyGURqvyyRhae8OhnUhv_ypBe-h9g/edit#gid=218712123
3. place the csv in the same directory as script.
4. rename the csv to “feedback.csv”
5. run the script on feedback.csv
6. this will generate a tex file called evaluation.tex 
7. run latex on evaluation.tex
8. you have your evaluation pdf



##to dos to refine this script: 

1. Write code quality items in a “student friendly” format in the html form, e.g. UTF-8 not used -> The project does not use UTF-8 for character encoding.
2. add version number in the html form
3. add help text “\par”  \\ for newline in personalmessage field. 
4. prefilled suggestions for each of the “suggestion fields” in the form. 
5. download the csv file from the script. 
6. rename the generated file to incorporate the coursename, version and studentname
7. give user the ability to choose the student name, so that csv can have more than one student information. 
8. fix the code so that latex runs without errors. 
9. write code for exceeds specifications. 
10. run the latex file through python to generate pdf. 
