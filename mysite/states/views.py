from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.shortcuts import render
from os.path import join
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

def index(request):
    return HttpResponse("Hello, world. You're at the State Data Viewing index.")

from .display import InputForm
from .models import STATES_DICT, YEARS_DICT, DATA_DICT, ID_DICT, DT_DICT
import pandas as pd
import os
import mpld3
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

def make_plot(SD_list, start_year, end_year, display_type, intersect_data):
    dlist = []
    for state, data in SD_list:
        if state not in ('', 'None') and data not in ('', 'None'):
            dlist.append((pd.read_csv(join(settings.STATIC_ROOT, 'states/', "{}.csv".format(data)), usecols = ["Year", state], index_col = "Year")
                        .rename(columns = {state : "{} in {}".format(DATA_DICT[data], STATES_DICT[state])})))
    indexes = list(range(int(start_year), int(end_year) + 1))
    if dlist != []:
        join_type = 'inner' if intersect_data == 'True' else 'outer'
        dlist = [d.ix[indexes] for d in dlist]
        df = pd.concat(dlist,
                        axis = 1,
                        join = join_type)
        if intersect_data == 'True': df.dropna(inplace = True)
    else: return "<p> Nothing To See Here </p>"

    if display_type == "plot":
        fig, ax = plt.subplots()
        ax.plot(df)
        ymin, ymax = ax.get_ylim()
        ax.set_ylim(ymin, ymax* (1 + len(df.columns)/10))
        ax.legend(df.columns.values, loc=9)
        ax.set_xlabel('Year')
        return mpld3.fig_to_html(fig)

    elif display_type == "corrplot":
        df = df.corr()
        fig, ax = plt.subplots()
        cax = ax.matshow(df)
        fig.colorbar(cax)
        ax.set_xticklabels([''] + df.columns.values)
        ax.set_yticklabels([''] + df.columns.values)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
        return mpld3.fig_to_html(fig)

    elif display_type in ("table", "corrmatrix"):
        if display_type == "corrmatrix":
            df = df.corr()
        try : table = df.to_html(float_format = "%.3f", classes = "table table-striped", index_names = False)
        except: table = df.to_html()
        table = table.replace('border="1"','border="0"')
        table = table.replace('style="text-align: right;"', "")
        return table

def display(request):
    state1 = request.GET.get('state1', 'None')
    data1 = request.GET.get('data1', 'None')
    state2 = request.GET.get('state2', 'None')
    data2 = request.GET.get('data2', 'None')
    state3 = request.GET.get('state3', 'None')
    data3 = request.GET.get('data3', 'None')
    state4 = request.GET.get('state4', 'None')
    data4 = request.GET.get('data4', 'None')
    state5 = request.GET.get('state5', 'None')
    data5 = request.GET.get('data5', 'None')
    state6 = request.GET.get('state6', 'None')
    data6 = request.GET.get('data6', 'None')
    state7 = request.GET.get('state7', 'None')
    data7 = request.GET.get('data7', 'None')
    state8 = request.GET.get('state8', 'None')
    data8 = request.GET.get('data8', 'None')

    start_year = request.GET.get('start_year', '2000')
    end_year = request.GET.get('end_year', '2016')

    display_type = request.GET.get('display_type', 'plot')

    intersect_data = request.GET.get('intersect_data', 'True')

    params = {'form_action' : reverse_lazy('states:display'),
              'form_method' : 'get',
              'form' : InputForm({'state1' : state1, 'data1' : data1,
                                    'state2' : state2, 'data2' : data2,
                                    'state3' : state3, 'data3' : data3,
                                    'state4' : state4, 'data4' : data4,
                                    'state5' : state5, 'data5' : data5,
                                    'state6' : state6, 'data6' : data6,
                                    'state7' : state7, 'data7' : data7,
                                    'state8' : state8, 'data8' : data8,

                                    'start_year' : start_year, 'end_year' : end_year,
                                    'display_type' : display_type, 'intersect_data' : intersect_data}),
            'plot_source' : make_plot( ( (state1, data1), (state2, data2), (state3, data3), (state4, data4),(state5, data5), (state6, data6),(state7, data7), (state8, data8) ),
                                        start_year, end_year,
                                        display_type, intersect_data)
              }

    return render(request, 'form.html', params)
