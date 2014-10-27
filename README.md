#evaluation-generator
====================
generates latex for the evaluation based on the form responses. 

##system requirements
latex! 

##How to use this script:
1. Fill out the html form: https://docs.google.com/a/knowlabs.com/forms/d/1aCC1ckzEnd4qF1r6VvWGoiDW9HZuDk44ZN7vglHdgxw/viewform
2. run the script : python process_csv_to_create_latex.py "student name" version e.g. python process_csv_to_create_latex.py "David Siltamaki" 1
3. The script will ask you for your google id - please enter your knowlabs id in quotes: e.g. "janhavi@knowlabs.com"
4. Enter google password without quotes. 
5. The script will generate the pdf of the evaluation in your working directory. 


##to dos to refine this script: 


1. prefilled suggestions for each of the “suggestion fields” in the form. 
2. write code for exceeds specifications. 
