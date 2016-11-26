from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.shortcuts import render
from os.path import join
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def csv(request):

   import pandas as pd

   data_path = join(settings.STATIC_ROOT, 'myapp/FRED_LF.csv')

   df = pd.read_csv(data_path)
   table = df.to_html(float_format = "%.3f", classes = "table table-striped", index_names = False)
   table = table.replace('border="1"','border="0"')
   table = table.replace('style="text-align: right;"', "") # control this in css, not pandas.

   return HttpResponse(table)

from .forms import InputForm
from .models import STATES_DICT, YEARS_DICT, DATA_DICT
import pandas as pd
import os
import mpld3
import matplotlib.pyplot as plt
import numpy as np
def make_plot(s1 = "None", s2 = "None", s3 = "None", d1 = "None", d2 = "None", d3 = "None"):
    # import pandas as pd
    # data_path = join(settings.STATIC_ROOT, 'myapp/FRED_LF.csv')
    # df = pd.read_csv(data_path)
    # df = df[df["County/City"].str.contains(county.lower(), case = False)
    # return
    data_path1, data_path2, data_path3 = 0,0, 0
    dlist = []
    for f in os.listdir(join(settings.STATIC_ROOT, 'myapp/')):
        if d1 in f and s1 != "None": data_path1 = f
        if d2 in f and s2 != "None": data_path2 = f
        if d3 in f and s3 != "None": data_path3 = f
    print(data_path1, data_path2, data_path3)
    if data_path1: dlist.append(pd.read_csv(join(settings.STATIC_ROOT, 'myapp/', data_path1), usecols = ["Date", s1], index_col = "Date").rename(columns = {s1 : "{} in {}".format(DATA_DICT[d1], STATES_DICT[s1])}))
    if data_path2: dlist.append(pd.read_csv(join(settings.STATIC_ROOT, 'myapp/', data_path2), usecols = ["Date", s2], index_col = "Date").rename(columns = {s2 : "{} in {}".format(DATA_DICT[d2], STATES_DICT[s2])}))
    if data_path3: dlist.append(pd.read_csv(join(settings.STATIC_ROOT, 'myapp/', data_path3), usecols = ["Date", s3], index_col = "Date").rename(columns = {s3 : "{} in {}".format(DATA_DICT[d3], STATES_DICT[s3])}))
    fig, ax = plt.subplots()
    for d in dlist:
        d.set_index(d.index.to_datetime().year, inplace = True)
    if dlist != []:
        df = pd.concat(dlist, axis = 1, join = "inner")
        print(df)
        ax.plot(df)
        ymin, ymax = ax.get_ylim()
        ax.set_ylim(ymin, ymax*1.2)
        ax.legend(df.columns.values, loc=1)
    #print(df.head())

    #
            #ax.plot(x = d.index.to_datetime().year, y = d[d.columns[0]])
            #color, size = np.random.random((2, 200))
            #fig.plot(x = [1,2,3,4], y = [1,2,3,4])
            #ax.lines(xdata = [1,2,3,4], ydata = [1,2,3,4])
            #ax.grid(color='lightgray', alpha=0.7)
    return mpld3.fig_to_html(fig)

    # print(s1,s2,s3,d1,d2,d3)
    # df = pd.read_csv(data_path)
    # table = df.to_html(float_format = "%.3f", classes = "table table-striped", index_names = False)
    # table = table.replace('border="1"','border="0"')
    # table = table.replace('style="text-align: right;"', "") # control this in css, not pandas.
    #return "<p>howdy</p>"

def form(request):
    # year = request.GET.get('year', '2016')
    state1 = request.GET.get('state1', 'None')
    state2 = request.GET.get('state2', 'None')
    state3 = request.GET.get('state3', 'None')
    data1 = request.GET.get('data1', 'None')
    data2 = request.GET.get('data2', 'None')
    data3 = request.GET.get('data3', 'None')

    # if not data1 and year1:
    #     state1 = request.GET.get('state1', 'AL')
    #     state2 = request.GET.get('state2', 'AK')
    #     state3 = request.GET.get('state3', 'AZ')
    #     data1 = request.GET.get('data1', 'Civilian Labor Force')
    #     data2 = request.GET.get('data2', 'NA')
    #     data3 = request.GET.get('data3', 'POP')
    # if not state and year:
    #     state = request.POST.get('state', 'PA')
    #     year = request.POST.get('year', '2016')

    params = {'form_action' : reverse_lazy('myapp:form'),
              'form_method' : 'get',
              'form' : InputForm({'state1' : state1, 'state2' : state2, 'state3' : state3,
                                    'data1' : data1, 'data2' : data2, 'data3' : data3}),
            #   'state1' : STATES_DICT[state1],
            #   'state2' : STATES_DICT[state2],
            #   'state3' : STATES_DICT[state3],
            #   'data1' : DATA_DICT[data1],
            #   'data2' :3DATA_DICT[data2],
            #   'data3' : DATA_DICT[data3]
            'plot_source' : make_plot(state1, state2, state3, data1, data2, data3)
              #'year' : YEARS_DICT[year]
              }

    return render(request, 'form.html', params)
