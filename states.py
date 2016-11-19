import pandas as pd
import geopandas as gpd
import quandl
import matplotlib.pyplot as plt

quandl.ApiConfig.api_key = 'pzsR2vefkG2XPBZpVq3a'

geo_df = gpd.read_file("/Users/romar9393/PPHA30550/lectures/08/ex/data/cb_2015_us_state_20m.shp")
geo_df.set_index(geo_df["STATEFP"].astype(int), inplace = True)
contiguous =  (geo_df.index < 57)
contiguous &= (geo_df.index != 15)
contiguous &= (geo_df.index != 2)
geo_df = geo_df[contiguous]

ax = geo_df.to_crs(epsg=4269).plot()
ax.set_axis_off()
plt.show()

states = {'AK': 'Alaska',
'AL': 'Alabama',
'AR': 'Arkansas',
'AZ': 'Arizona',
'CA': 'California',
'CO': 'Colorado',
'CT': 'Connecticut',
'DC': 'District of Columbia',
'DE': 'Delaware',
'FL': 'Florida',
'GA': 'Georgia',
'HI': 'Hawaii',
'IA': 'Iowa',
'ID': 'Idaho',
'IL': 'Illinois',
'IN': 'Indiana',
'KS': 'Kansas',
'KY': 'Kentucky',
'LA': 'Louisiana',
'MA': 'Massachusetts',
'MD': 'Maryland',
'ME': 'Maine',
'MI': 'Michigan',
'MN': 'Minnesota',
'MO': 'Missouri',
'MS': 'Mississippi',
'MT': 'Montana',
'NC': 'North Carolina',
'ND': 'North Dakota',
'NE': 'Nebraska',
'NH': 'New Hampshire',
'NJ': 'New Jersey',
'NM': 'New Mexico',
'NV': 'Nevada',
'NY': 'New York',
'OH': 'Ohio',
'OK': 'Oklahoma',
'OR': 'Oregon',
'PA': 'Pennsylvania',
'RI': 'Rhode Island',
'SC': 'South Carolina',
'SD': 'South Dakota',
'TN': 'Tennessee',
'TX': 'Texas',
'UT': 'Utah',
'VA': 'Virginia',
'VT': 'Vermont',
'WA': 'Washington',
'WI': 'Wisconsin',
'WV': 'West Virginia',
'WY': 'Wyoming'}



# def makePanelData(db, pre, post, start_year, end_year):
#     df = pd.concat([get_data(db = "FRBNY", pre = "HDC_CCARD_", post = "", year = str(year)) for year in range(start_year, end_year)])
#         df =


dd = get_panel(FRED)
    for db, opts in db_dict.items()])
    df = getData(db = "FRBNY", pre = "HDC_CCARD_", post = "")
db_dict =  {"FRED" : ["LF", "NA", "POP"], # Labor particiption, Employees on payroll, Population
            "FRBNY" : ["HDC_STLOAN_", "HDC_CCARD_"], # student Loan Debt Balance Per Capita, Credit card debt  per capita
            "NCES" : ["SCHOOLS_FRGRADS_"]}  # ??? freshman graduation rate Full state name
FRED = {"db" : "FRED", "pre_post" : [["","LF"],["", "NA"], ["","POP"]]}
df = df.transpose()
geo_merge = geo_df.join(df.ix["2015"], on = "NAME", how = "inner")
geo_merge.set_index("NAME")["2015"].sort_values(ascending = False).plot(kind = "bar", figsize = (15, 3))
plt.show()


ft = "2015"
albers = geo_merge.to_crs(epsg=2163)
ax = albers.plot(column = ft, scheme = "quantiles", k = 5, cmap = "PuOr", legend = True,
                 alpha = 0.4, linewidth = 0.5, figsize = (12, 8))

ax.set_title("STUDENT LOANS 2015", fontsize = 30)
ax.set_axis_off()
plt.show()
