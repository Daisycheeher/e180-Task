#importing libs
import urllib.request as request
import json
from pathlib import Path

#accessing the api and loading data
with request.urlopen('https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita') as response:
        if response.getcode() == 200:
            source = response.read()
            data = json.loads(source)
        else:
            print('An error occurred while attempting to retrieve data from the API.')
#print(json.dumps(data))
from functools import singledispatch

#funcion to check null values and remove it
@singledispatch
def remove_null_bool(ob):
    return ob

@remove_null_bool.register(list)
def _process_list(ob):
    return [remove_null_bool(v) for v in ob]

@remove_null_bool.register(dict)
def _process_list(ob):
    return {k: remove_null_bool(v) for k, v in ob.items()
            if v is not None and v is not True and v is not False}

#newd=json.dumps(remove_null_bool(data), indent=4, sort_keys=True)

newd=str(data)
print(type(newd))

import ast
#newd=data
#creating literable data
my_dict=ast.literal_eval(newd)

#records = [{x: [{"ingredient": x["strIngredient1"]}, {"measure": x["strMeasure1"]}]} for x in my_dict["drinks"]]

#converting to bool value 
bool_alc=lambda val: True if val=="Alcoholic" else False
bool_conf=lambda val: True if val=="Yes" else False

new_dict={}
my_list=[]

#print(my_dict["drinks"])
import datetime
#import pytz

#utc to iso time conversion
def conv_utc_iso8601(time_str):
    d = datetime.datetime.strptime(time_str, '%d/%m/%Y %H:%M:%S')
    # add proper timezone
    pst = pytz.timezone('America/Los_Angeles')
    d = pst.localize(d)
    return d.isoformat()

for i in my_dict["drinks"]:
    inst_dict={}
    inst_dict["en"]=i['strInstructions']
    inst_dict["de"]=i['strInstructionsDE']

    name_dict={}
    name_dict["en"]=i['strDrink']

    new_dict["id"]=i['idDrink']
    new_dict["name"]=name_dict
    new_dict["category"]=i['strCategory']
    new_dict["alcoholic"]=bool_alc(i['strAlcoholic'])
    new_dict["glass"]=i['strGlass']
    new_dict["instructions"]=inst_dict
    new_dict["thumbnail"]=i['strDrinkThumb']
    new_dict["creativeCommonsConfirmed"]=bool_conf(i['strCreativeCommonsConfirmed'])
    new_dict["dateModified"]=i['dateModified']
    my_list.append(new_dict)
#print(my_list)

final_dict={}
final_dict["drinks"]=my_list
example_path = Path('test.json')
opt=json.dumps(remove_null_bool(final_dict), indent=4, sort_keys=False)
example_path.write_text(opt, encoding='utf-8')
