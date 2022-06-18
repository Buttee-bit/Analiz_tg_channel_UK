from multiprocessing import context
import pandas as pd
import json
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    context = {
        
    }
    return render(request,'dashboard/index.html',context)
