import quandl
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
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

#def getData(db, pre, post, state_name = False, state_dict = states):
    #df = pd.concat([quandl.get("{}{}{}{}{}".format(db, "/", pre, name.upper() if state_name else abv, post)).rename(columns = {"Amount" : name}) for abv, name in states.items()],
                   #axis = 1) #data frame type needs to also be listed
    #df.index = ["{}_{}{}".format(year, pre, post) for year in df.index.year]
    #return df

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
    return quandl.get(url)

def getTotalColumns(tr_list):
    return {tr_list[1] : [int(re.sub("[^0-9]", "", n)) for n in tr_list if "," in n or n.isdigit()]}

def getCensusData(state):
    base_url = "http://censusviewer.com/state/"
    soup = BeautifulSoup(requests.get(base_url + state).content)
    soup = soup.find("table", attrs = {"class" : "data_table"})
    data_dict = {}
    for i in soup.find_all("tr"):
        t = getTotalColumns(i.text.split("\n"))
        if list(t.values()) != [[]]: data_dict.update(t)
    return pd.DataFrame(data_dict).transpose().rename(columns = {0 : "2010", 1 : "2000", 2 : "2000 - 2010 Change"})

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

for db in data_dict:
    for info in data_dict[db]:
        full_data = []
        for state in states:
            getCensusData(state).to_csv("CENSUS_{}.csv".format(state))
            data = getQuandlData(db, info, state)
            full_data.append(data.rename(columns = {data.columns[0] : state}))
        final_data = pd.concat(full_data, axis = 1);
        data.index = pd.DatetimeIndex(data.index).year
        final_data.to_csv(db + "_" + info + ".csv", encoding='utf-8');
