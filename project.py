import sys
import os
import csv
import requests
import shutil
import secrets
from PIL import Image
from alive_progress import alive_bar
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import jinja2

CWD = os.getcwd()


def main():
    print("Welcome to the cocktail recipe builder!")
    check_sys_args(sys.argv, len(sys.argv))
    drinks_to_query = collect_input(sys.argv[1])
    print(f"{len(drinks_to_query)} drinks found in file. Looking for recipes...")
    with alive_bar(len(drinks_to_query)) as bar:
        for _ in compute(drinks_to_query):
            bar()
    cleanup()
    print("Done!")


"""
Helper function to generate callback for the progressbar

Input:
    - list of drinks to query in the api
Output:
    - a recipe in .docx format for each cocktail that has been found in the api
    - progress callback for the progressbar
"""
def compute(drinks):
    for drink in drinks:
            recipe = get_drink_recipe(drink)
            if recipe is not None:
                create_docx(recipe)
            yield


"""
Checks for correct function call, otherwise exits

Input:
    - input file
    - length of argv list
Output:
    - exits if prohibited
    - return 1 valid input
"""
def check_sys_args(argv, argv_len):
    # check for correct length
    if argv_len != 2:
        sys.exit("Usage: python project.py filepath")

    # check if input file exits
    if not os.path.exists(argv[1]):
        sys.exit("The file or path you provided doesn't exist")

    # check for the correct file extension
    if os.path.splitext(argv[1])[1] not in [".txt", ".csv"]:
        sys.exit("Only .txt and .csv files are supported input")

    # return 1 for success
    return 1

"""
Collects all of the drinks from the input files and format's them

Input:
    - input file
Output:
    - list of all the drinks found in the file
    - exits if file doesn't exist
"""
def collect_input(argv):
    try:
        drinks = []
        with open(argv, encoding="utf-8-sig") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                for column in row:
                    # format input
                    c = column.strip()
                    if c != '':
                        drinks.append(c.lower().replace(' ', '_'))
        return drinks           
    except FileNotFoundError:
        sys.exit("The file or path you provided was deleted")


"""
Querys the Cocktail DB for a drink 

Input:
    - the drink name to query (random for random drink)
Output:
    - a dict containing all the information or None if no drink was found
"""
def get_drink_recipe(drink_name):
    # get cocktail data from api
    if drink_name != "random":
        r = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink_name}")
    else:
        r = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/random.php")

    # exit if api not reachable
    if r.status_code != 200:
        sys.exit("The API is not recable at the moment, try again later")

    # return none if no data found, return formatted dict otherwise
    data = r.json()
    try:
        cocktail = data["drinks"][0]
    except TypeError:
        return None
    recipe = {}

    recipe["name"] = cocktail["strDrink"]
    recipe["instructions"] = cocktail["strInstructions"]
    recipe["glass"] = cocktail["strGlass"]
    for i in range(1,16):
        if cocktail[f"strIngredient{i}"] is not None:
            recipe[f"ingredient{i}"] = cocktail[f"strIngredient{i}"]
            recipe[f"measure{i}"] = cocktail[f"strMeasure{i}"]

    # get cocktail image
    url = cocktail["strDrinkThumb"]
    r = requests.get(url, stream=True)
    # create temp folder and random file name
    if not os.path.exists(f"{CWD}/temp"):
        os.makedirs(f"{CWD}/temp")
    file_path = f"{CWD}/temp/{secrets.token_hex(16)}.jpg"

    with open(file_path, "wb") as out_file:
        shutil.copyfileobj(r.raw, out_file)
    del r
    recipe["image"] = file_path

    # resize image
    with Image.open(file_path) as im:
        size = (300, 300)
        im.thumbnail(size, Image.LANCZOS)
        im.save(file_path)

    return recipe

"""
Creates a .docx file from the received information

Input: 
    - a dict containing all the infos about a cocktail
Output:
    - a formatted word document
"""
def create_docx(recipe):
    # create output folder
    if not os.path.exists(f"{CWD}/recipes"):
        os.makedirs(f"{CWD}/recipes")

    # open template
    tpl = DocxTemplate(f"{CWD}/utils/template.docx")

    # create page context
    context = {
        "title": recipe["name"],
        "image": InlineImage(
            tpl, recipe["image"], width=Mm(80), height=Mm(80)
        ),
        "tbl_contents" : [
        ],
        "glass" : recipe["glass"],
        "desc" : recipe["instructions"]
    }
    for i in range(1,16):
        try:
            entry = {"measure": recipe[f'measure{i}'], "ingredient": recipe[f'ingredient{i}']}
            context["tbl_contents"].append(entry)
        except KeyError:
            continue 

    # insert content into page
    jinja_env = jinja2.Environment(autoescape=True)
    tpl.render(context, jinja_env)
    tpl.save(f"{CWD}/recipes/{recipe['name']}.docx")


"""
Deletes the temp folder that is created to temporarily save the cocktail images
"""
def cleanup():
    # delete temp folder
    shutil.rmtree(f"{CWD}/temp")

if __name__ == "__main__":
    main()