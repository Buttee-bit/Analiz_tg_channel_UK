import os
import docx
import re
import pandas as pd
import numpy as np
import pickle

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer as snow

from sklearn.feature_extraction.text import  TfidfVectorizer



from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect


# Create your views here


def index(request):
    global attributied, name
    if request.method == "POST":
        uploaded_file = request.FILES['document']
        if uploaded_file.name.endswith('.docx'):
            # save csv file in media folder
            savefile = FileSystemStorage()

            name = savefile.save(uploaded_file.name, uploaded_file)  # this is a name file

            # know where to save file
            d = os.getcwd()  # Current directory of the project
            file_directiry = d + '\media\\' + name
            readfile(file_directiry)
            return redirect(results)
    else:
        pass

    return render(request, 'dashboard/index.html')


##project.csv

def readfile(filename):
    ## Объявление глобальных переменных
    global model, path_document, \
        data_norm, list_text_doc, len_doc_paragraph, \
        df_docx, dict_class_color, \
        list_values_mount, dict_week

    ## Чтение и обрабока данных


    #data_norm = normalize_data()
    def get_model(path_model):
        with open(path_model, 'rb') as file:
            pickle_model = pickle.load(file)
        return pickle_model
    model = get_model(r'model\LinearSVC_model_2700.pkl')

    ##  Создание графика распределения по дням для каждой группы
    def load_file(path_to_file):
        doc = docx.Document(path_to_file)
        all_paragraphs = doc.paragraphs
        list_text_doc = [par.text for par in all_paragraphs]
        len_doc_paragraph = len(all_paragraphs)
        return list_text_doc, len_doc_paragraph
    list_text_doc,len_doc_paragraph = load_file('media\\' + name)

    def get_dict_class_to_color(path_color):
        dict_class_color ={}
        df = pd.read_csv(path_color)
        df.index = df['Unnamed: 0']
        f_1 = df['f1-score']
        for class_, value in zip(f_1.index, f_1.values):
            if value < .25:
                dict_class_color[class_] = 'black'
            if value < .5 and value > .25:
                dict_class_color[class_] = 'brown'
            if value < .75 and value > 0.5:
                dict_class_color[class_] = 'green'
            if value > .75:
                dict_class_color[class_] = 'blue'

        return dict_class_color


    dict_class_color = get_dict_class_to_color('model\\'+ 'df_class_rep.csv')
    print(dict_class_color)
    #list_keys_valuse_counts, list_values_valuse_counts = get_list_value_counts(data_norm)
    def pandas_df_text(text_doc):
        df = pd.DataFrame(text_doc, columns=['text'])
        return df

    df_docx = pandas_df_text(list_text_doc)
    ## Создание графика распределения сообщений по дням месяца
    def clear_text(text):
        stop_words = set(stopwords.words('russian'))
        text_cleaning_re = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
        tokens = []
        text = re.sub(text_cleaning_re, ' ', str(text).lower()).strip()
        text = re.sub(r'\s+', ' ', text)
        for token in text.split():
            if token not in stop_words:
                token = "".join(c for c in token if token.isalnum())
                if len(token) != 2:
                    tokens.append(token)
        return " ".join(tokens)

    def pre_process(text):
        stemmer = snow('russian')
        tokens = []
        for token in text.split():
            tokens.append(stemmer.stem(token))
        return " ".join(tokens)

    texts_ = df_docx.text.apply(lambda x: clear_text(x))
    texts_stemm = texts_.apply(lambda x: pre_process(x))

    #list_keys_mount, list_values_mount = get_list_key_value_mount(data_norm)
#Возвращает словарь в котором обозначено в каком параграфе какой класс
    def tfidf_text(texts_stemm):
        tfidf_doc = TfidfVectorizer(max_features=2745, ngram_range=(1, 4))
        X = tfidf_doc.fit_transform(texts_stemm)
        Ypredict = model.predict(X)
        Ypredict = Ypredict.tolist()
        range_ = [i for i in range(len(Ypredict))]
        dict_ = {}
        for i in range_:
            dict_[i] = Ypredict[i]
        return dict_
    dict_ = tfidf_text(texts_stemm)

    #dict_week = value_for_week(data_norm)


def results(request):

    #list_k_Monday = dict_week['Monday'][0]
    #list_v_Monday = dict_week['Monday'][1]
    #list_k_Saturday = dict_week['Saturday'][0]
    #list_v_Saturday = dict_week['Saturday'][1]
    #list_k_Sunday = dict_week['Sunday'][0]
    #list_v_Sunday = dict_week['Sunday'][1]
    #list_k_Thursday = dict_week['Thursday'][0]
    #list_v_Thursday = dict_week['Thursday'][1]
    #list_k_Tuesday = dict_week['Tuesday'][0]
    #list_v_Tuesday = dict_week['Tuesday'][1]
    #list_k_Wednesday = dict_week['Wednesday'][0]
    #list_v_Wednesday = dict_week['Wednesday'][1]
    #list_k_Friday = dict_week['Friday'][0]
    #list_v_Friday = dict_week['Friday'][1]

    context = {
        #'list_keys_mount': list_keys_mount,
        #'list_values_mount': list_values_mount,
        #'list_keys_valuse_counts': list_keys_valuse_counts,
        #'list_values_valuse_counts': list_values_valuse_counts,
        #'list_k_Monday': list_k_Monday,
        #'list_v_Monday': list_v_Monday,
        #'list_k_Saturday': list_k_Saturday,
        #'list_v_Saturday': list_v_Saturday,
       # 'list_k_Sunday': list_k_Sunday,
        #'list_v_Sunday': list_v_Sunday,
        #'list_k_Thursday': list_k_Thursday,
        #'list_v_Thursday': list_v_Thursday,
        #'list_k_Tuesday': list_k_Tuesday,
        #'list_v_Tuesday': list_v_Tuesday,
        #'list_k_Wednesday': list_k_Wednesday,
        #'list_v_Wednesday': list_v_Wednesday,
        #'list_k_Friday': list_k_Friday,
        #'list_v_Friday': list_v_Friday
    }
    return render(request, 'dashboard/results.html', context)

def nlp_results(request):
    list_path_photo = []
    return render(request,'dashboard/nlp_results.html')