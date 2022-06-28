import os

import pandas as pd
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect


# Create your views here


def index(request):
    global attributied
    if request.method == "POST":
        uploaded_file = request.FILES['document']
        if uploaded_file.name.endswith('.csv'):
            # save csv file in media folder
            savefile = FileSystemStorage()

            name = savefile.save(uploaded_file.name, uploaded_file)  # this is a name file

            # know where to save file
            d = os.getcwd()  # Current directory of the project
            file_directiry = d + '\media\\' + name
            readfile(file_directiry)
            return redirect(results)
    else:
        messages.warning(request, 'File was not uploaded. Please use csv file extension !')

    return render(request, 'dashboard/index.html')


##project.csv

def readfile(filename):
    ## Объявление глобальных переменных
    global list_keys_valuse_counts, list_values_valuse_counts, \
        data_norm, my_file, list_keys_to_week, \
        list_values_to_week, list_keys_mount, \
        list_values_mount

    ## Чтение и обрабока данных
    def normalize_data(data):
        data = pd.read_csv('news_tg_bess.csv')
        data['date_time'] = data['date'] + ' ' + data['time']
        data['date_time'] = pd.to_datetime(data['date_time'])
        data.index = data['date_time']
        data = data.drop(columns=['date', 'time'], axis=1)
        data = data.drop(columns=['md5'], axis=1)
        data = data.drop(columns=['image'], axis=1)
        data = data.drop(columns=['messageLink'], axis=1)
        data = data.drop(columns=['messageImage'], axis=1)
        data = data.drop(columns=['forwardedChanel'], axis=1)

        return data

    data_norm = normalize_data(filename)
    print(data_norm)
    ##  Создание графика распределения по дням для каждой группы
    def get_list_value_counts(data_norm):
        data_counts = data_norm.groupby('chanel', as_index=False).agg({
            "id": 'count'
        }).sort_values('id', ascending=False)
        list_keys_valuse_counts = []
        list_values_valuse_counts = []
        for key, value in zip(data_counts['chanel'], data_counts['id']):
            list_keys_valuse_counts.append(key)
            list_values_valuse_counts.append(value)
        return list_keys_valuse_counts, list_values_valuse_counts

    list_keys_valuse_counts, list_values_valuse_counts = get_list_value_counts(data_norm)

    ## Создание графика распределения сообщений по дням месяца
    def get_list_key_value_mount(data_norm):
        data_norm_M = data_norm.resample('d').id.nunique().to_frame(name='mount_count')
        data_norm_M['Day'] = data_norm_M.index.day
        list_keys_mount = list(data_norm_M.Day.unique())
        list_values_mount = list(data_norm_M.mount_count)
        return list_keys_mount, list_values_mount

    list_keys_mount, list_values_mount = get_list_key_value_mount(data_norm)

    def value_for_week(data_norm):

        day_week = dict
        list = []
        list_keys_to_week = []
        list_values_to_week = []

        data_to_week = pd.DataFrame(data=data_norm, index=None)
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

        for key, value in zip(data_monday['hour'], data_monday['day_hour_count']):
            list_keys_to_week.append(key)
            list_values_to_week.append(value)

        return list_keys_to_week, list_values_to_week

    list_keys_to_week, list_values_to_week = value_for_week(data_norm)


def results(request):
    context = {
        'list_keys_mount': list_keys_mount,
        'list_values_mount': list_values_mount,
        'list_keys_valuse_counts': list_keys_valuse_counts,
        'list_values_valuse_counts': list_values_valuse_counts,
        'list_keys_to_week': list_keys_to_week,
        'list_values_to_week': list_values_to_week
    }
    print(context)
    return render(request, 'dashboard/results.html', context)
