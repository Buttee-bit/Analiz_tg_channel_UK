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
import datetime

# Create your views here


def index(request):

    global attributied
    if request.method =="POST":
        uploaded_file = request.FILES['document']
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
    global columns,column_valuse_counts,\
        data,my_file,data_counts,\
        data_to_week,data_monday


    my_file = pd.read_csv(filename)
    
    data = pd.DataFrame(data=my_file,index=None)
    data_counts = data.groupby('chanel', as_index=False).agg({
                               "Unnamed: 0":'count'
                              }).sort_values('Unnamed: 0',ascending=False)
  
  
    data_to_week = pd.DataFrame(data=my_file,index=None)
    data_to_week['date_time'] = pd.to_datetime(data_to_week['date_time'])
    data_to_week['dow'] = data_to_week.date_time.dt.day_name()
    data_to_week['hour'] = data_to_week.date_time.dt.hour

    data_to_week = data_to_week.groupby([
        'dow',
        'hour'
    ]).hour.count().to_frame(name='day_hour_count')
    data_to_week = data_to_week.reset_index()
    # Сюда вставить цикл по дням недели
    data_monday = data_to_week[data_to_week['dow'] == 'Monday']


def results(request):
# Создание первого графика общего распределения
    column_valuse_counts = []

    list_keys_valuse_counts = []
    list_values_valuse_counts = []

    for i in data_counts:
        column_valuse_counts.append(i)
    
    for key,value in zip(data_counts[f'{column_valuse_counts[0]}'],data_counts[f'{column_valuse_counts[1]}']):
        list_keys_valuse_counts.append(key)
        list_values_valuse_counts.append(value)
# Создание графиков распределения по дням недели
    
    def get_list_keys_values_to_week(data_to_day):
        column = []
        list_keys_to_week = []
        list_values_to_week = []
        for i in data_to_day:
            column.append(i)

    # test = [keys,values in zip(data_to_day[f'{column[1]}'], data_to_day[f'{column[1]}'])]
        for key, value in zip(data_to_day[f'{column[1]}'], data_to_day[f'{column[2]}']):
            list_keys_to_week.append(key)
            list_values_to_week.append(value)

        return list_keys_to_week,list_values_to_week

    list_keys_to_week, list_values_to_week = get_list_keys_values_to_week(data_monday)
# Итоговая переменная передающаяся во фронт

    context = {
        'list_keys_valuse_counts': list_keys_valuse_counts,
        'list_values_valuse_counts': list_values_valuse_counts,
        'list_keys_to_week':list_keys_to_week,
        'list_values_to_week':list_values_to_week
    }
    print(context)

    return render(request,'dashboard/results.html',context)