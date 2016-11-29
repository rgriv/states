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
            final_data.to_csv("mysite/static/states/" + db + "__" + info + ".csv", encoding='utf-8');

######CENSUS#######
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
        typeDict[dataType].to_csv("mysite/static/states/" + re.sub("__", "", group) + "_" + slugify(dataType) + ".csv", encoding='utf-8')

######GOVERNMENT SPENDING#######
def getSpendingStateTypeData(state, data_type):
    #data_types = ['bn', 'dn', 'pn']
    year_dict = {}
    for year in range(2000, 2016):
        url = "http://www.usgovernmentspending.com/year_download_{}{}{}_18bc2n#usgs302".format(year, state, data_type)
        soup = BeautifulSoup(requests.get(url).content)
        soup =  soup.find_all("tr", attrs = {"class" : "tier"}) + soup.find_all("tr", attrs = {"class" : "tiere"})
        data_dict = {}
        for x in soup:
            try:
                x = list(x.children)
                data_dict[x[1].text.replace(':\xa0 Start chart',"")] = float(x[-2].text.replace('\xa0', ""))
            except: pass
        year_dict[str(year)] = pd.Series(data_dict)
    df = pd.DataFrame(year_dict).transpose()
    df.index.name = "Year"
    return(df)

def getSpendingDataSets(data_type, folder):
    for state in states.keys():
        print(state)
        getSpendingStateTypeData(state, data_type).to_csv("{}{}_{}{}".format(folder, data_type, state, ".csv"))

getSpendingDataSets("pn", "Raw Spending/")
getSpendingDataSets("bn", "Raw Spending/")
getSpendingDataSets("dn", "Raw Spending/")

def formatSpendingData(folder, end_folder):
    spending_types = ["Balance", "Education", "General Government",
                    "Gross Public Debt", "Health Care", "Interest",
                    "Other Borrowing", "Other Spending", "Pensions",
                    "Protection", "Total Spending", "Transportation", "Welfare"]
    for data_type in ["bn", "pn", "dn"]:
        for st in spending_types:
            df_list = []
            for state, name in states.items():
                df = pd.read_csv("{}{}_{}.csv".format(folder, data_type, state), usecols = ["Year", st], index_col = "Year")
                df_list.append(df.rename(columns = {st : state}))
            pd.concat(df_list, axis = 1).to_csv("{}{}_{}.csv".format(end_folder, data_type, st))
formatSpendingData("Raw Spending/", "mysite/static/myapp/")
