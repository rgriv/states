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
def make_plot(s1, s2, s3, d1, d2, d3):
    # import pandas as pd
    # data_path = join(settings.STATIC_ROOT, 'myapp/FRED_LF.csv')
    # df = pd.read_csv(data_path)
    # df = df[df["County/City"].str.contains(county.lower(), case = False)
    # return
    import pandas as pd

    data_path = join(settings.STATIC_ROOT, 'myapp/FRED_LF.csv')

    df = pd.read_csv(data_path)
    table = df.to_html(float_format = "%.3f", classes = "table table-striped", index_names = False)
    table = table.replace('border="1"','border="0"')
    table = table.replace('style="text-align: right;"', "") # control this in css, not pandas.
    return table

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
            'plot_source' : make_plot(STATES_DICT[state1], STATES_DICT[state2], STATES_DICT[state3], DATA_DICT[data1], DATA_DICT[data2], DATA_DICT[data3])
              #'year' : YEARS_DICT[year]
              }

    return render(request, 'form.html', params)
