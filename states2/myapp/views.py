# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.shortcuts import render

# from django.urls import reverse # future versions.
from django.core.urlresolvers import reverse_lazy


from os.path import join
from django.conf import settings

import numpy as np, pandas as pd
import matplotlib.pyplot as plt

import requests

from .forms import InputForm
from .models import STATEFP_DICT, STATES_DICT, CURRENCY_DICT

import geopandas as gpd, folium
from geopy import Nominatim

import seaborn as sns
sns.set(font_scale = 1.7)

from io import BytesIO

def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def table(request):

    df = pd.DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])
    table = df.to_html(float_format = "%.3f", classes = "table table-striped", index_names = False)
    table = table.replace('border="1"','border="0"')
    table = table.replace('style="text-align: right;"', "") # control this in css, not pandas.

    return HttpResponse(table)


def pure_template(req):

  params = {"xli" : ["Bessy", "has", "fantastic", "cats"],
            "animal" : "dog",
            "di" : {"dog" : "woof", "cat" : "meow", "tiger" : "roar"}}
  ### if we change "animal" : "cat", to "animal" : "cat", >>> "Poor choice of animal" will be printed
  return render(req, "pure_template.html", params)


def csv(request, year = None):


   filename = join(settings.STATIC_ROOT, 'myapp/va_presidential.csv')

   df = pd.read_csv(filename)

   if year: df = df[df["Year"] == int(year)]

   table = df.to_html(float_format = "%.3f", classes = "table table-striped", index_names = False)
   table = table.replace('border="1"','border="0"')
   table = table.replace('style="text-align: right;"', "") # control this in css, not pandas.

   return HttpResponse(table)


def greet(request, w):

    return HttpResponse("Well hello, {}!".format(w))


def add(request, p1, p2):

    p1 = int(p1)
    p2 = int(p2)

    return HttpResponse("{} + {} = {}".format(p1, p2, p1 + p2))


def greet_template(req, w):

  return render(req, "greet.html", {"who" : w})


from .forms import CountiesForm
def display_table(request):
    #http://127.0.0.1:8000/myapp/display_table/        will display 'Accomack County' as the default
    #http://127.0.0.1:8000/myapp/display_table/?county=Alexandria+City   will display Alexandria+City
    county = request.GET.get('county', 'Accomack County')
    #state = request.GET.get('state', 'California')

    filename = join(settings.STATIC_ROOT, 'myapp/va_presidential.csv')
    df = pd.read_csv(filename)

    # select data from rows with "County/City"] == county
    df = df[df["County/City"] == county]

    if not df.size: return HttpResponse("No such county!")
    #print("##### debug: display_table()")
    #print(df);
    table = df.to_html(float_format = "%.3f", classes = "table table-striped", index = False)
    table = table.replace('border="1"','border="0"')
    table = table.replace('style="text-align: right;"', "") # control this in css, not pandas.

    params = {'title' : county,
              'form_action' : reverse_lazy('myapp:display_pic'),
              'form_method' : 'get',
              'form' : CountiesForm({'county' : county}),
              #'form': StatesForm({'state': state}),
              'html_table' : table}

    return render(request, 'view_table.html', params)


def get_reader(request): # note: no other params.

  address = request.GET.get('address', 'ADDR')  # if we knew the parameters ...
  state = request.GET.get('state', 'STATE')  # if we knew the parameters ...
  zipc = request.GET.get('zipc', 'ZIP')  # if we knew the parameters ...
  d = dict(request.GET._iterlists())

  return HttpResponse(str(d))


def form(request):
    state = request.GET.get('state', 'PA')
    address = request.GET.get('address', 'Liberty Bell')
    currency = request.GET.get("currency", "EUR")
    # if not state: state = request.POST.get('state', 'PA')


    #location = str(g.geocode(STATES_DICT[state])._point[:2])

    ## Nominatim (from the Latin, 'by name') is a tool to search OSM data by name or address
    ## OSM stands for OpenStreetMap
    g = Nominatim()
    location = str(g.geocode(address)._point[:2])

    params = {'form_action' : reverse_lazy('myapp:form'),
              'form_method' : 'get',
              'form' : InputForm({'state' : state, 
                                  'address' : address,
                                  'currency': currency}),
              'state' : STATES_DICT[state], 
              'location' : location}
              # 'currency' : CURRENCY_DICT[currency]}

    return render(request, 'form.html', params)


from django.views.generic import FormView
class FormClass(FormView):
    # http://127.0.0.1:8000/myapp/formclass/?address=2121+Ornellas+dr%2C+milpitas&state=CA
    # http://127.0.0.1:8000/myapp/formclass/     --- default will provide PA
    template_name = 'form.html'
    form_class = InputForm


    def get(self, request):

      state = request.GET.get('state', 'PA')

      return render(request, self.template_name, {'form_action' : reverse_lazy('myapp:formclass'),
                                                  'form_method' : 'get',
                                                  'form' : InputForm({'state' : state}),
                                                  'state' : STATES_DICT[state]})

    def post(self, request):

      state = request.POST.get('state', 'PA')

      return render(request, self.template_name, {'form_action' : reverse_lazy('myapp:formclass'),
                                                  'form_method' : 'get',
                                                  'form' : InputForm({'state' : state}),
                                                  'state' : STATES_DICT[state]})



def pic(request, c = None):

   t = np.linspace(0, 2 * np.pi, 30)
   u = np.sin(t)

   plt.figure() # needed, to avoid adding curves in plot
   plt.plot(t, u, color = c)

   # write bytes instead of file.
   figfile = BytesIO()

   # this is where the color is used.
   try: plt.savefig(figfile, format = 'png')
   except ValueError: raise Http404("No such color")

   figfile.seek(0) # rewind to beginning of file
   return HttpResponse(figfile.read(), content_type="image/png")


from .forms import CountiesForm
def display_pic(request, c = 'r'):
    ## http://127.0.0.1:8000/myapp/display_pic/      default display Accomack County
    ## http://127.0.0.1:8000/myapp/display_pic/?county=Albemarle+County
    county = request.GET.get('county', 'Accomack County')

    params = {'title' : county,
              'form_action' : reverse_lazy('myapp:display_pic'),
              'form_method' : 'get',
              'form' : CountiesForm({'county' : county}),
              'pic_source' : reverse_lazy("myapp:plot", kwargs = {'c' : county})}

    return render(request, 'view_pic.html', params)


def plot(request, c = "Accomack County"):
   filename = join(settings.STATIC_ROOT, 'myapp/va_presidential.csv')

   df = pd.read_csv(filename, index_col = "Year", parse_dates = ["Year"])

   df = df[df["County/City"] == c]
   if not df.size: return HttpResponse("No such county!")

   df["Democratic Share"] = 100 - df["Republican Share"]

   ax = df[["Democratic Share", "Republican Share"]].plot(color = ["b", "r"])
   ax.set_ylabel("Percent of Two-Party Vote")

   # write bytes instead of file.
   figfile = BytesIO()

   # this is where the color is used.
   plt.subplots_adjust(bottom = 0.16)
   try: ax.figure.savefig(figfile, format = 'png')
   except ValueError: raise Http404("No such color")

   figfile.seek(0) # rewind to beginning of file
   return HttpResponse(figfile.read(), content_type="image/png")


def resp_redirect(request):

    state = request.POST.get('state', '')
    if not state: state = request.GET.get('state', '')

    if state: return HttpResponseRedirect(reverse_lazy('myapp:resp', kwargs = {'state' : state}))

    return HttpResponseRedirect(reverse_lazy('myapp:form'))


def resp(request, state):
    return HttpResponse("I hear you, {}.".format(STATES_DICT[state]))


def static_site(request):
  return render(request, "static_site.html")


def leaflet_population(request):
  return render(request, "leaflet_population.html")


# this is a sample for using matplotlib
def smom_map(request):
    from shapely.affinity import translate, rotate, scale
    import geopandas as gpd

    filename = join(settings.STATIC_ROOT, 'myapp/cb_2015_us_state_20m.shp')

    geo_df = gpd.read_file(filename)


    geo_df.plot()

    geo_df.set_index(geo_df["STATEFP"].astype(int), inplace=True)
    geo_df.head(5)

    contiguous = (geo_df.index < 57)    ### only 50 states
    #contiguous &= (geo_df.index != 15)  ### Skip Hawaii
    #contiguous &= (geo_df.index != 2)   ### Skip Alaska
    geo_df = geo_df[contiguous]


    # geo_df.set_index("NANME", inplace=True)
    # geo_df.set_value("Hawaii", "geometry", translate(geo_df.ix["Hawaii", "geometry"], 53, 5))
    # For Alaska, you'll probably have to chop off the smallest of the Aleutian Islands
    # (which are in the Eastern Hemisphere, and "wrap around").  So you have to get rid
    # of several of the polygons (islands) in the MultiPolygon of Alaska.  Those are
    # so small I wouldn't worry about them.
    #geo_df.ix["Alaska"].geometry[10:]

    # The current index of the table is "STATEFP"
    # This is to reduce some of the points of the polygons from Alaska
    #geo_df.ix[2].geometry[10:]
    #geo_df.set_value(2, "geometry", translate(geo_df.ix[2, "geometry"], 0, -20))

    ## THis is to move Hawaii closer
    #geo_df.set_value(15, "geometry", translate(geo_df.ix[15, "geometry"], 20, 5))

    #geo_df.plot()
    #print(geo_df.crs)

    #ax = geo_df.to_crs(epsg=2163).plot()
    #ax.set_axis_off()


    j = requests.get("http://api.census.gov/data/2014/acs5/profile?for=state:*&get=DP02_0037PE").json()
    smom_df = pd.DataFrame(j[1:], columns=j[0])
    smom_df["state"] = smom_df["state"].astype(int)
    smom_df.set_index("state", inplace=True)
    smom_df["DP02_0037PE"] = smom_df["DP02_0037PE"].astype(float)
    smom_df.rename(columns={"DP02_0037PE": "Percent Mothers Unmarried"},
                   inplace=True)
    smom_df.head()

    geo_merge = geo_df.join(smom_df, how="inner")

    geo_merge.set_index("NAME")["Percent Mothers Unmarried"].sort_values(ascending=False).plot(kind="bar", figsize=(15, 3))

    ft = "Percent Mothers Unmarried"

    # try 2163 (albers), 3857 (web), 4269 (plate)
    albers = geo_merge.to_crs(epsg=2163)
    ## k=4 mean labels color is divided by 4.
    ax = albers.plot(column=ft, scheme="quantiles", k=4, cmap="PuOr", legend=True, alpha=0.4, linewidth=0.5, figsize=(12, 8))

    ax.set_title("Percent Single Mothers", fontsize=30)
    ax.set_axis_off()

    from io import BytesIO
    figfile = BytesIO()
    ax.get_figure().savefig(figfile, format='png')
    figfile.seek(0) # rewind to beginning of file
    return HttpResponse(figfile.read(), content_type="image/png")


def embedded_map2(request):
    filename = join(settings.STATIC_ROOT, 'myapp/TM_WORLD_BORDERS_SIMPL-0.3.shp')

    m = folium.Map([39.828175, -98.5795], tiles='stamenwatercolor', zoom_start=1)

    df = gpd.read_file(filename)

    mountains = ["Aconcagua", "Mount Kosciuszko", "Mont Blanc, Chamonix", "Mount Everest", "Denali", "Mount Elbrus",
                 "Puncak Jaya", "Mount Kilimanjaro", "Mount Vinson"]
    #mtn_df = gpd.tools.geocode(mountains, provider="googlev3").to_crs(df.crs)

    mtn_df = gpd.tools.geocode(["London", "Paris", "New York", "Hong Kong", "San Francisco", "Tokyo"])

    folium.GeoJson(gpd.sjoin(df, mtn_df, how="inner", op="contains"),
                   style_function=lambda feature: {
                       'fillColor': 'red', 'fillOpacity': 0.6, 'weight': 2, 'color': 'black'
                   }).add_to(m)

    for xi, pt in mtn_df.iterrows():
        folium.RegularPolygonMarker(pt.geometry.coords[::][0][::-1], popup=pt.address,
                                    number_of_sides=5, radius=8, fill_color="black", fill_opacity=1.0).add_to(m)

    map_string = m._repr_html_().replace("width:100%;", "width:60%;float:right;", 1)

    return render(request, 'view_map.html', {"title": "Test Map2",
                                             "map_string": map_string})


def embedded_map3(request):
    filename = join(settings.STATIC_ROOT, 'myapp/cb_2015_us_state_500k.shp')
    #filename = join(settings.STATIC_ROOT, 'myapp/tl_2016_us_county.shp') ## not useable, take too long to load

    # map = folium.Map(location=[48, -102], zoom_start=3)
    #m = folium.Map([39.828175, -98.5795], tiles='stamenwatercolor', zoom_start=1)
    m = folium.Map([39.828175, -98.5795], zoom_start=3)

    df = gpd.read_file(filename)

    city_df = gpd.tools.geocode(["New York", "San Francisco", "Honolulu", "Anchorage" ])

    folium.GeoJson(gpd.sjoin(df, city_df, how="inner", op="contains"),
                   style_function=lambda feature: {
                       'fillColor': 'blue', 'fillOpacity': 0.6, 'weight': 2, 'color': 'black'
                   }).add_to(m)

    ## This is to mark the location for each city
    for xi, pt in city_df.iterrows():
        folium.RegularPolygonMarker(pt.geometry.coords[::][0][::-1], popup=pt.address,
                                    number_of_sides=5, radius=8, fill_color="green", fill_opacity=1.0).add_to(m)

    map_string = m._repr_html_().replace("width:100%;", "width:60%;float:right;", 1)

    return render(request, 'view_map.html', {"title": "Test Map3", "map_string": map_string})


def smom_folium(request):
    import requests, pandas as pd
    import geopandas as gpd

    filename = join(settings.STATIC_ROOT, 'myapp/cb_2015_us_state_20m.shp')

    geo_df = gpd.read_file(filename)
    geo_df.plot()

    geo_df.set_index(geo_df["STATEFP"].astype(int), inplace=True)
    geo_df.head(5)

    contiguous = (geo_df.index < 57)
    # contiguous &= (geo_df.index != 15)
    # contiguous &= (geo_df.index != 2)
    geo_df = geo_df[contiguous]
    geo_df.plot()

    j = requests.get("http://api.census.gov/data/2014/acs5/profile?for=state:*&get=DP02_0037PE").json()
    smom_df = pd.DataFrame(j[1:], columns=j[0])
    smom_df["state"] = smom_df["state"].astype(int)
    smom_df.set_index("state", inplace=True)
    smom_df["DP02_0037PE"] = smom_df["DP02_0037PE"].astype(float)
    smom_df.rename(columns={"DP02_0037PE": "Percent Mothers Unmarried"}, inplace=True)
    smom_df.head()
    #print(smom_df)
    geo_merge = geo_df.join(smom_df, how="inner")

    geo_merge.set_index("NAME")["Percent Mothers Unmarried"].sort_values(ascending=False).plot(kind="bar",
                                                                                               figsize=(15, 3))

    ft = "Percent Mothers Unmarried"

    #########################################
    # Below are for interactive map
    ########################################
    import folium

    m = folium.Map([39.828175, -98.5795], tiles='cartodbpositron', zoom_start=4, max_zoom=14, min_zoom=4)

    ft = "Percent Mothers Unmarried"
    cmap = folium.colormap.linear.YlOrRd.scale(geo_merge[ft].min(), geo_merge[ft].max())

    folium.GeoJson(geo_merge,
                   style_function=lambda feature: {'fillColor': cmap(feature['properties'][ft]), 'fillOpacity': 0.6,
                                                   'weight': 2, 'color': 'black'}).add_to(m)

    cmap.caption = 'Percent Children Born to Single Mothers'
    cmap.add_to(m)

    #m.save("us_single_mothers.html")
    #m
    map_string = m._repr_html_().replace("width:90%;", "height:60%;float:top;", 1)

    return render(request, 'view_states.html', {"title": "Interactive Single Mom Map",
                                             "map_string": map_string})


def election(request):
    # Pennsylvania Election Returns¶
    # Import pandas and geopandas, and the democratic vote shares from the last election.
    # See Advanced.ipynb for the (not actually very advanced) scraping from the PA elections site.
    import pandas as pd, geopandas as gpd

    ## Read csv file for the vote % in each county
    filename = join(settings.STATIC_ROOT, 'myapp/pa_demshare.csv')
    demvote_df = pd.read_csv(filename, index_col="county")
    demvote_df.head()  # DataFrame.head(n=5) Returns first n rows

    ## Read geo (county) data from cb_2015_us_county_20m.shp
    filename = join(settings.STATIC_ROOT, 'myapp/cb_2015_us_county_20m.shp')
    counties = gpd.read_file(filename)
    counties["lname"] = counties["NAME"].str.lower()
    counties = counties[counties["STATEFP"] == "42"].set_index("lname")


    ## Merge the cvs and geo (shp) data
    merged = counties.join(demvote_df, how="inner")

    ax = counties.plot()
    ax.set_axis_off()

    # Let's again make a Choropleth map, this time with equal_interval.
    # This time, an appropriate CRS is 3651, for southern Pennsylvania (spatial reference).
    # Other epsg value 2163 (albers), 3857 (web), 4269 (plate)
    # albers = geo_merge.to_crs(epsg=2163)

    ft = "Democratic Two-Party Vote Share"
    ax = merged.to_crs(epsg=3651).plot(scheme="EQUAL_INTERVAL", k=9, column=ft,
                                       figsize=(23, 12), legend=True, cmap="rainbow")
    ax.set_axis_off()

    ax.set_title(ft, fontsize=30)

    from io import BytesIO
    figfile = BytesIO()
    ax.get_figure().savefig(figfile, format='png')
    figfile.seek(0) # rewind to beginning of file
    return HttpResponse(figfile.read(), content_type="image/png")


def population(request):
    import requests, pandas as pd
    import geopandas as gpd

    filename = join(settings.STATIC_ROOT, 'myapp/cb_2015_us_state_20m.shp')

    geo_df = gpd.read_file(filename)
    geo_df.plot()

    geo_df.set_index(geo_df["STATEFP"].astype(int), inplace=True)
    geo_df.head(5)

    contiguous = (geo_df.index < 57)
    # contiguous &= (geo_df.index != 15)
    # contiguous &= (geo_df.index != 2)
    geo_df = geo_df[contiguous]
    geo_df.plot()


    filename = join(settings.STATIC_ROOT, 'myapp/states_population.csv')
    pop_df = pd.read_csv(filename)
    #pop_df = pd.read_csv(filename, index_col=0, thousands=",", skiprows=[1])  # read all data

    pop_df["state"] = pop_df["state"].astype(int)
    pop_df.set_index("state", inplace=True)
    pop_df["2015"] = pop_df["2015"].astype(int)
    #pop_df.rename(columns={"DP02_0037PE": "Percent Mothers Unmarried"}, inplace=True)
    pop_df.head()
    geo_merge = geo_df.join(pop_df, how="inner")
    geo_merge.set_index("NAME")["2015"].sort_values(ascending=False).plot(kind="bar", figsize=(15, 3))
    ft = "2015"

    #########################################
    # Below are for interactive map
    ########################################
    import folium

    m = folium.Map([39.828175, -98.5795], tiles='cartodbpositron', zoom_start=4, max_zoom=14, min_zoom=4)


    # GeoJSON is an open standard format designed for representing simple geographical
    # features, along with their non-spatial attributes, based on JavaScript Object
    # Notation encoding a variety of geographic data structures.
    # GeoJSON supports the following geometry types: Point, LineString, Polygon,
    # MultiPoint, MultiLineString, and MultiPolygon. Geometric objects with additional
    # properties are Feature objects.
    #
    # Sets of features are contained by FeatureCollection objects.
    # Specification: http://geojson.org/geojson-spec.html
    # {
    #  "type": "Feature",
    #  "geometry": {
    #    "type": "Point",
    #    "coordinates": [125.6, 10.1]
    #  },
    #  "properties": {
    #    "name": "Dinagat Islands"
    #  }
    #}

    # sequential color palettes choices are:  Greys, Blues, YIGnBu, YlOrRd
    cmap = folium.colormap.linear.YlOrRd.scale(geo_merge[ft].min(), geo_merge[ft].max())

    folium.GeoJson(geo_merge,
                   style_function=lambda feature: {'fillColor': cmap(feature['properties'][ft]), 'fillOpacity': 0.6,
                                                   'weight': 2, 'color': 'black'}).add_to(m)

    cmap.caption = 'United States Population'
    cmap.add_to(m)

    #m.save("us_single_mothers.html")
    #m
    map_string = m._repr_html_().replace("width:90%;", "width:40%;float:left;", 1)

    return render(request, 'view_states.html', {"title": "United States Population","map_string": map_string})


def folium_sample1(request):
    import requests, pandas as pd
    import geopandas as gpd
    import json
    import os
    import folium

    #print(folium.__version__)

    #filename = os.path.join('data', 'us-states.json')
    filename = join(settings.STATIC_ROOT, 'myapp/us-states.json')

    geo_json_data = json.load(open(filename))
    m = folium.Map([43, -100], zoom_start=4)

    folium.GeoJson(geo_json_data).add_to(m)

    # Instead of saving to a html file, we prepare a map_string
    #       m.save(os.path.join('results', 'GeoJSON_and_choropleth_0.html'))
    map_string = m._repr_html_().replace("width:90%;", "height:60%;float:top;", 1)
    return render(request, 'view_states.html', {"title": "folium_sample", "map_string": map_string})


def heat_map(request):
    from folium.plugins import HeatMap
    import numpy as np
    import json

    #filename = os.path.join('data', 'us-states.json')
    filename = join(settings.STATIC_ROOT, 'myapp/us-states.json')

    geo_json_data = json.load(open(filename))
    m = folium.Map([43, -100], zoom_start=4)

    folium.GeoJson(geo_json_data).add_to(m)

    # randomly generate 100 data points around coordinate [43, -100]
    data = (np.random.normal(size=(100, 3)) *
            np.array([[1, 1, 1]]) +
            np.array([[43, -100, 1]])).tolist()

    #print(data)  # print to console for debugging

    HeatMap(data).add_to(m)
    # Instead of saving to a html file, we prepare a map_string
    # m.save(os.path.join('data', 'Heatmap.html'))
    map_string = m._repr_html_().replace("width:90%;", "height:60%;float:top;", 1)
    return render(request, 'view_states.html', {"title": "Heat Map Sample", "map_string": map_string})



def show_PA_state(request):
    # Pennsylvania Election Returns¶
    # Import pandas and geopandas, and the democratic vote shares from the last election.
    # See Advanced.ipynb for the (not actually very advanced) scraping from the PA elections site.
    import pandas as pd, geopandas as gpd

    ## Read csv file for the vote % in each county
    filename = join(settings.STATIC_ROOT, 'myapp/pa_demshare.csv')
    demvote_df = pd.read_csv(filename, index_col="county")
    demvote_df.head()  # DataFrame.head(n=5) Returns first n rows

    ## Read geo (county) data from cb_2015_us_county_20m.shp
    filename = join(settings.STATIC_ROOT, 'myapp/cb_2015_us_county_20m.shp')
    counties = gpd.read_file(filename)
    counties["lname"] = counties["NAME"].str.lower()
    counties = counties[counties["STATEFP"] == "42"].set_index("lname")

    ## Merge the cvs and geo (shp) data
    merged = counties.join(demvote_df, how="inner")

    ax = counties.plot()
    ax.set_axis_off()

    # Let's again make a Choropleth map, this time with equal_interval.
    # This time, an appropriate CRS is 3651, for southern Pennsylvania (spatial reference).
    # Other epsg value 2163 (albers), 3857 (web), 4269 (plate)
    # albers = geo_merge.to_crs(epsg=2163)

    ft = "Democratic Two-Party Vote Share"
    ax = merged.to_crs(epsg=3651).plot(scheme="EQUAL_INTERVAL", k=9, column=ft,
                                       figsize=(23, 12), legend=True, cmap="rainbow")

    g = Nominatim()
    m = folium.Map(g.geocode("Pennsylvania")._point[:2], zoom_start=6)

    # sequential color palettes choices are:  Greys, Blues, YIGnBu, YlOrRd
    cmap = folium.colormap.linear.YlOrRd.scale(merged[ft].min(), merged[ft].max())

    folium.GeoJson(merged,
                   style_function=lambda feature: {'fillColor': cmap(feature['properties'][ft]), 'fillOpacity': 0.6,
                                                   'weight': 2, 'color': 'black'}).add_to(m)

    cmap.caption = 'Democratic Share'
    cmap.add_to(m)

    # Instead of saving to a html file, we prepare a map_string
    #       m.save(os.path.join('results', 'GeoJSON_and_choropleth_0.html'))
    map_string = m._repr_html_().replace("width:90%;", "height:60%;float:top;", 1)
    return render(request, 'view_states.html', {"title": "State-County Map", "map_string": map_string})


from .forms import StatesForm
def display_state(request, s = 'r'):
    ## http://127.0.0.1:8000/myapp/display_state/      default display CA
    ## http://127.0.0.1:8000/myapp/display_state/?state=CA
    state = request.GET.get('state', 'CA')

    statefp = STATEFP_DICT[state]
    state_name = STATES_DICT[state]

    ## Read geo (county) data from cb_2015_us_county_20m.shp
    filename = join(settings.STATIC_ROOT, 'myapp/cb_2015_us_county_20m.shp')
    counties = gpd.read_file(filename)
    counties["lname"] = counties["NAME"].str.lower()
    counties["STATEFP"] = counties["STATEFP"].astype(int)
    counties = counties[counties["STATEFP"] == statefp].set_index("lname")

    ft = "State: " + state_name + " Map"

    g = Nominatim()
    m = folium.Map(g.geocode(state_name)._point[:2], zoom_start=6)

    folium.GeoJson(counties).add_to(m)

    map_string = m._repr_html_().replace("width:90%;", "height:60%;float:top;", 1)
    return render(request, 'view_states.html', {"title": ft, "map_string": map_string})

