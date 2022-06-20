from cgi import print_form
from multiprocessing import context
from optparse import Values
from typing import Counter
import pandas as pd
import json
from django.http import JsonResponse
from django.shortcuts import render , redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import os

# Create your views here


def index(request):

    global attributied
    if request.method =="POST":
        uploaded_file = request.FILES['document']
        attributied = request.POST.get('attributeid')
        print(attributied)
        if uploaded_file.name.endswith('.csv'):
            #save csv file in media folder 
            savefile = FileSystemStorage()

            name = savefile.save(uploaded_file.name, uploaded_file) # this is a name file
            
            #know where to save file
            d = os.getcwd() # Current directory of the project
            file_directiry = d+'\media\\'+name
            readfile(file_directiry)
            return redirect(results)
    else:
        messages.warning(request, 'File was not uploaded. Please use csv file extension !')

    return render(request,'dashboard/index.html')



 ##project.csv

def readfile(filename):
    global rows,columns,data,my_file,data_counts


    my_file = pd.read_csv(filename)
    
    data = pd.DataFrame(data=my_file,index=None)
    data_counts = data.groupby('chanel', as_index=False).agg({
                               "Unnamed: 0":'count'
                              }).sort_values('Unnamed: 0',ascending=False)

            
def results(request):
    column = []
    data_pie_counts = []

    listkeys = []
    listvalues = []
    for i in data_counts:
        column.append(i)
    for key,value in zip(data_counts[f'{column[0]}'],data_counts[f'{column[1]}']):
        listkeys.append(key)
        listvalues.append(value)

    context = {
        'listkeys': listkeys,
        'listvalues': listvalues,
    }
    print(context)

    return render(request,'dashboard/results.html',context)