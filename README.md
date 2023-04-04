# Cocktail Recipe Generator - CS50P Final Project

## Short Description

Have you ever wondered how your favorite cocktails are made? Or do you need new inspiration for cocktails? 
No worries! Give this program a list of your cocktails or the word "random" and get beautifully formatted recipes back.

## Package Description

Here you can see an overview of all the external libraries use in the code, and how they're used:

    - alive_progress
        Displays and animated progressbar while files are created

    - docx, docxtpl and python_docx:
        Are used in order to interact and generate the .docx output

    - Jinja2
        In order to create a word document a template is used. In order to fill the predefined template Jinja2 is used

    - Pillow
        Pillow is used to scale and compress the images returned from the API

    - requests
        Is used to call the API

Everything you need to install is listed in the requirements.txt and can be installed using the following command-line prompt:

    pip install -r /path/to/requirements.txt

## Where do we get the recipes from 

    In order to get all the images and the recipe data this project uses the [Cocktail DB](https://www.thecocktaildb.com/), which is an API that delivers instructions on how to make cocktails.

## Allowed input and usage

    The correct usage for the programm is:

        python project.py file.csv

    file.csv can be either a .csv or a .txt file that contains all the drink names you want to query. These need to be seperated by a comma (,). If you want a recipe of
    a random drink you add "random" to a file like a drink as often as you like.

    The program searches for all your drink in the API and if something is found and the corresponding in images is saved in a folder named temp that occurs while you run the program. This folder will be deleted automaticly after the run. So please don't change anything manually.

    The output can then be accessed through the recipe folder.

## Files included

The following files are included in the project folder:

    - project.py 
        Includes the main python file to execute the program

    - test_project.py 
        Can be used with pytest to test some aspects of the program

    - requirements.txt
        Contains all the external libraries need for the program

    - utils/template.docx
        the template that used to create the output file
        
    - utils/test_input
        example input files that can be used to test the project

## Video demonstration

    [See a short video here](TODO)

## Acknowledgements

    Thanks to the CS50 team for the amazing course on python. I learned a lot and hope you're happy with my final project :wink:

