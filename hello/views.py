import re
from django.utils.timezone import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from hello.models import listOfDownloads
from django.views.generic import ListView

import requests
import json
#NOTE resign of pandas, use only petl
import pandas as pd
import petl as etl

print('http://127.0.0.1:8000/')

#---Home view definition----displaying Tables here:listOfDownloads ---------
class HomeListView(ListView):
    """Renders the home page, with a list of all loads."""
    model = listOfDownloads
    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

#---Fetch---------------------------------------------------------------------
def fetch(request):
    # request API
    r = requests.get ('https://swapi.dev/api/people/')
    swapiData= r.json()

    #json to petl table----------------------------------------
    #keys= list( swapiData['results'][0].keys() )
    keys=['name', 'birth_year', 'homeworld','edited']
    data=json.dumps(swapiData['results'])
    with open('MyJsonfile.json', 'w') as f:
        f.write(data)
    table0 = etl.fromjson('MyJsonfile.json', header=keys)
    #get the next jsons
    response=requests.get(swapiData['next'])
    table_full = table0
    if response.status_code == 200:
        r_next = requests.get (swapiData['next'])
        swapiData_next= r_next.json()
        keys=['name', 'birth_year', 'homeworld','edited']
        data=json.dumps(swapiData_next['results'])
        with open('MyJsonfile_next.json', 'w') as f:
            f.write(data)
        table0_next = etl.fromjson('MyJsonfile_next.json', header=keys)
        #print(response.status_code) 
        table_full = etl.mergesort(table_full, table0_next, key='name')
        response=requests.get(swapiData_next['next'])
    #table_full contain all data

    #--1-correct 'edited' field-----------------------
    # convert values under the given field using a regular expression substitution.
    table1 = etl.sub(table_full, field='edited', pattern='T', repl=' ', 
    count=0, flags=0)

    #--2-Add a date column based on edited date--------------
    table2 = etl.split(table1, 'edited', ' ', ['date', 'time'])

    #--3-Resolve the homeworld field into the homeworld's name-----
    #Download the planet names always with the data in case mapping gets changed
    def readPlanet(url):
        r = requests.get (url=url)
        HomeWorld= r.json()
        planetName=HomeWorld["name"]
        return planetName

    table3 = etl.convert(table2, 'homeworld', readPlanet)
    #--final touch: cutout time coll and save to csv
    table4 = etl.cutout(table3, 'time')

    #save as csv 
    current_time = datetime.now()
    time_stamp = current_time.timestamp()
    name= str (int (time_stamp) ) + '.csv'
    etl.tocsv(table4, name)

    #saving meta data
    new_load = listOfDownloads(file_name = str(name))
    new_load.save()

    return redirect("home")

#---Table view-----------------------------------------------------------------------------

def tablelayout(request,file,rowNumber):
    df = pd.read_csv(file)
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data[:rowNumber], "csv_name": file, "row_number":rowNumber}
    return render(request, 'hello/tablelayout.html', context)

#------------- Show more view ---------------------------------------------

def showMore(request,file, rowNumber):
    rowNumber += 10
    #NOTE add communicate when file has no more rows
    return tablelayout(request,file,rowNumber)    


#------------- Value counts view -----------------------------------------------------------------------------

def tableValCan(request,file,rowNumber):
    #NOTE change pandas to petl
    df = pd.read_csv(file)
    columns=[]
    if request.method == 'POST':
        columns = request.POST.getlist('columns')
    else:
        return HttpResponse("wybierz kolumny")
    #NOTE change pandas to petl
    dfCounts= df.value_counts(subset=columns)    

    json_records = dfCounts.reset_index().to_json(orient ='records')
    with open('json_records.json', 'w') as f:
        f.write(json_records)
    data = []
    data = json.loads(json_records)

    #prepare headers names for table
    headerDict={'name':'Name',
    	    'birth_year':'Birth year',
        	'homeworld':'Homeworld',
            'date':	'Date'}
    headers = [headerDict[x] for x in columns]
    headers.append('Count')
    #prepare columns list to improve loop over columns in value_counts.html
    #columns.append('0') then add columns to context
    #rows=['birth_year','homeworld','0']  then add rows to context
    #last comma is necessary
    context = {'d': data, "csv_name": file, "header":headers,   }
    return render(request, 'hello/value_counts.html', context)


