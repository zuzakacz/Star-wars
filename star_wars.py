import requests
import json
import pprint
import pandas as pd
import datetime
import petl as etl


# star_wars.py

r = requests.get ('https://swapi.dev/api/people/')
swapiData= r.json()
#json to petl table----------------------------------------
#keys= list( swapiData['results'][0].keys() )
keys=['name', 'birth_year', 'homeworld','edited']

data=json.dumps(swapiData['results'])
with open('MyJsonfile.json', 'w') as f:
    f.write(data)

table0 = etl.fromjson('MyJsonfile.json', header=keys)
print(table0) 

response=requests.get(swapiData['next'])
#print(response.status_code)
table_full = table0
if response.status_code == 200:
    r_next = requests.get (swapiData['next'])
    swapiData_next= r_next.json()
    keys=['name', 'birth_year', 'homeworld','edited']
    data=json.dumps(swapiData_next['results'])
    with open('MyJsonfile_next.json', 'w') as f:
        f.write(data)
    table0_next = etl.fromjson('MyJsonfile_next.json', header=keys)
    print(response.status_code)
    print(table0_next) 
    table_full = etl.mergesort(table_full, table0_next, key='name')
    response=requests.get(swapiData_next['next'])

print(table_full.lookall()) 


'''
#--1-correct edited datetime field-----------------------
print("---------------1----------------------------------")
# Convenience function to convert values under the given field using 
# a regular expression substitution. See also re.sub().
table1 = etl.sub(table0, field='edited', pattern='T', repl=' ', 
count=0, flags=0)
print(table1) 

#--2-Add a date column based on edited date--------------
print("----------------2--------------------------------")
table2 = etl.split(table1, 'edited', ' ', ['date', 'time'])
print(table2)

#--3-Resolve the homeworld field into the homeworld's name-----
#Download the planet names always with the data in case mapping get changed
print("---------------3---------------------------------")
def readPlanet(url):
    r = requests.get (url=url)
    HomeWorld= r.json()
    planetName=HomeWorld["name"]
    #print(planetName)
    return planetName

table3 = etl.convert(table2, 'homeworld', readPlanet)
print(table3) 



#--final touch: cutout time coll and save to csv
print("---------------4----------------------------------")
table4 = etl.cutout(table3, 'time')
print(table4) 
etl.tocsv(table4, 'example.csv')


#to juz niepotrzebne:
#isodate = etl.dateparser('%Y-%m-%d')
#table3 = etl.convert(table1, 'edited', isodate)
#print(table3) 


'''




'''
# Writing sample.json

with open("sample.json", "w") as f:
    f.write(json_object)

print("-------OK-----------------")

Extract data from a JSON file. 
The file must contain a JSON array as the top level object, 
and each member of the array will be treated as a row of data. E.g.:

#json file
data = 
    [{"foo": "a", "bar": 1},
     {"foo": "b", "bar": 2},
     {"foo": "c", "bar": 2}]
     
     with open('example.file1.json', 'w') as f:
     f.write(data)
   
    table1 = etl.fromjson('example.file1.json', header=['foo', 'bar'])
    table1




petlTable1 = etl.fromjson("sample.json")

petlTable = etl.fromcsv("data_loaded_1676031625.csv")
print(petlTable)

print("================2==OK==================")


print("---------------next -----------------------------------------------")
print(swapiData ['next'])

print("---------------SWAPI data frame -----------------------------------")
swapiString=json.dumps(swapiData['results'])
swapiDF= pd.read_json(swapiString)
swapiDF=swapiDF.drop( labels = [ 'height', 'mass', 'hair_color', 'skin_color', 'eye_color',
        'gender',  'films', 'species', 'vehicles','starships',  'url'], axis =1)   
print (swapiDF.head() )


current_time = datetime.datetime.now()
time_stamp = current_time.timestamp()
name=str(int (time_stamp))
print(time_stamp)
print(name)
print('data_loaded'+name+'.csv')
print(swapiDF.columns)
print("--------------------------------------------")


formatted_now = current_time.strftime("%A, %d %B %Y at %X")
formatted_now = current_time.strftime("%Y-%m-%d")
print(formatted_now)

'''
