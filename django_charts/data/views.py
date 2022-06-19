from multiprocessing import context
import pandas as pd
import json
from django.http import JsonResponse
from django.shortcuts import render , redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import os

# Create your views here


def index(request):
    if request.method =="POST":
        uploaded_file = request.FILES['document']

        if uploaded_file.name.endswith('.csv'):
            #save csv file in media folder 
            savefile = FileSystemStorage()

            name = savefile.save(uploaded_file.name, uploaded_file) # this is a name file
            
            #know where to save file
            d = os.getcwd() # Current directory of the project
            file_directiry = d+'\media\\'+name
            return redirect(results)
    else:
        messages.warning(request, 'File was not uploaded. Please use csv file extension !')

    return render(request,'dashboard/index.html')

def readfile(filename):
    pass
            
def results(request):
    return render(request,'results.html')