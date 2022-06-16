import pandas as pd
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts.html', {})


def get_data(request, *args, **kwargs):
    df = pd.read_csv('data_tg.csv')
    json_data = df.to_json()
    parsed = json.loads(json_data)

    return JsonResponse(parsed)  # http response
