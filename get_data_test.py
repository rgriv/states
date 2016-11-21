import quandl
import pandas as pd
#scrape http://censusviewer.com/state/AL
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

def getData(db, info, state_abv):
    url = "{}/{}{}";
    print(info);
    if db == "FRED":
        url = url.format(db, state, info)
    elif db == "FRBNY":
        url = url.format(db, info, state);
    else:
        url = url.format(db, info, states[state_abv].upper())
    print(url);
    return quandl.get(url)
    #return (url, quandl.get(url))

for db in data_dict:
    for info in data_dict[db]:
        full_data = []
        for state in states:
            data = getData(db, info, state)
            column_names = [d + " in " + state for d in data.columns]
            data.columns = column_names
            full_data.append(data)
        final_data = pd.concat(full_data, axis = 1);
        final_data.to_csv(db + "__" + info + ".csv", encoding='utf-8');
        #print(final_data);
        #data = pd.concat([getData(db, info, state).rename(columns = {"Amount": state}) for state in states], axis = 1);

#def get_panel(db_dict):
    #for pre, post in db_dict["pre_post"]:
        #print (getData(db_dict["db"], pre, post, db_dict["state"]))
    #return pd.concat([getData(db_dict["db"], pre, post, db["state"]) for pre, post in db_dict["pre_post"]])


# for abv, name in states.items:
#     for data_suffix in data_suffixs[:1]:
#         df = quandl.get(data_prefix + "/" + abv + data_suffix)
#         df.ix[dt.datetime(2005, 1, 1) : dt.datetime(2015, 12, 31)]
#         print(abv)
#         print(df.index)
