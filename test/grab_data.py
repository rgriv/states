import quandl
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import sys
import os

quandl.ApiConfig.api_key = 'pzsR2vefkG2XPBZpVq3a'
states = {
'AK': 'Alaska',
'AL': 'Alabama',
'AR': 'Arkansas',
'AZ': 'Arizona',
'CA': 'California',
'CO': 'Colorado',
'CT': 'Connecticut',
'DC': 'DistrictofColumbia',
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
'NC': 'NorthCarolina',
'ND': 'NorthDakota',
'NE': 'Nebraska',
'NH': 'NewHampshire',
'NJ': 'NewJersey',
'NM': 'NewMexico',
'NV': 'Nevada',
'NY': 'NewYork',
'OH': 'Ohio',
'OK': 'Oklahoma',
'OR': 'Oregon',
'PA': 'Pennsylvania',
'RI': 'RhodeIsland',
'SC': 'SouthCarolina',
'SD': 'SouthDakota',
'TN': 'Tennessee',
'TX': 'Texas',
'UT': 'Utah',
'VA': 'Virginia',
'VT': 'Vermont',
'WA': 'Washington',
'WI': 'Wisconsin',
'WV': 'WestVirginia',
'WY': 'Wyoming'}

data_dict = {"FRED" : ["LF", "NA", "POP"], # Labor particiption, Employees on payroll, Population, post
"FRBNY" : ["HDC_STLOAN_", "HDC_CCARD_"], # student Loan Debt Balance Per Capita, Credit card debt  per capita, state abbreviation pre
"NCES" : ["SCHOOLS_FRGRADS_"]}  # ??? freshman graduation rate Full state name, pre

# we need a way to convert data to valid filenames
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    return value
#
# slice by data type
def sliceByType(df):
    #figure out num of columns per state
    cols = list(df.columns.values)
    cols = [item[4:] for item in cols]
    # get unique column names without state
    seen = set()
    cols = [x for x in cols if not (x in seen or seen.add(x))]
    # there will be df per data type
    typeDict = {}
    for dataType in cols:
        finalCols = [state + ": " + dataType for state in states]
        finalDf = df[finalCols]
        finalDf.columns = [col[:2] for col in finalDf.columns]
        typeDict[dataType] = finalDf

    return typeDict

######QUANDL#######
if (not os.path.exists("QUANDL")):
    os.mkdir("QUANDL")

def getQuandlData(db, info, state_abv):
    url = "{}/{}{}"
    print(info)
    if db == "FRED":
        url = url.format(db, state, info)
    elif db == "FRBNY":
        url = url.format(db, info, state);
    elif db == "NCES":
        url = url.format(db, info, states[state_abv].upper())
    else:
        print("No database with that name.")
    print(url)
    return quandl.get(url, collapse="annual")

for db in data_dict:
    for info in data_dict[db]:
        full_data = []
        for state in states:
            data = getQuandlData(db, info, state)
            column_names = [state + ": " + d for d in data.columns]
            data.columns = column_names
            full_data.append(data)
        final_data = pd.concat(full_data, axis = 1);
        final_data.index = final_data.index.year
        final_data.index.name = "Year"

        if (db == "NCES"):
            typeDict = sliceByType(final_data)
            for dataType in typeDict:
                typeDict[dataType].to_csv("QUANDL/" + db + "_" + info + "_" + slugify(dataType) + ".csv", encoding='utf-8');
        else:
            final_data.columns = [x[:2] for x in final_data.columns]
            final_data.to_csv("QUANDL/" + db + "__" + info + ".csv", encoding='utf-8');

######CENSUS#######
if (not os.path.exists("CENSUS")):
    os.mkdir("CENSUS")
def getColumnValues(td_list):
    #return [td_list[0], [int(re.sub("[^0-9]", "", n)) for n in td_list if "," in n or n.isdigit()]]
    return [int(re.sub("[^0-9]", "", n)) for n in td_list if "," in n or n.lstrip("-").isdigit()]

census_groups = ["__total", "race", "latino", "gender", "agemunge"];

def getCensusData(state):
    base_url = "http://censusviewer.com/state/"
    census_data = dict.fromkeys(census_groups)
    print("Parsed " + state)
    soup = BeautifulSoup(requests.get(base_url + state).content, "html.parser")
    #soup = BeautifulSoup(open(state + ".html"), "html.parser")
    soup = soup.find("table", attrs = {"class" : "data_table"})
    df_index = ["2010", "2000", "change"];
    values = {}
    for group in census_groups:
        census = pd.DataFrame(index = df_index)
        for i in soup.find_all(name="tr", class_ = "data_body " + group):
            # df per census group
            td_list = [td.text for td in i.find_all("td")]
            column = pd.DataFrame({state + ": " + td_list[0]: getColumnValues([td.text for td in i.find_all("td")])}, df_index)
            census = pd.concat([census, column], axis=1)
            census.index.name = "Year"

        census_data[group] = census

    return census_data

final_census = dict.fromkeys(census_groups)
for state in states:
    census_dict = getCensusData(state)
    for key in census_dict:
        final_census[key] = pd.concat([final_census[key], census_dict[key]], axis=1);

#create csv for each census group
for group in census_groups:
    # remove change row
    df = final_census[group]
    df = df.drop(df.index[len(df)-1])
    typeDict = sliceByType(df)
    for dataType in typeDict:
        typeDict[dataType].to_csv("CENSUS/" + re.sub("__", "", group) + "_" + slugify(dataType) + ".csv", encoding='utf-8')
