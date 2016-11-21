import quandl
#scrape http://censusviewer.com/state/AL
quandl.ApiConfig.api_key = 'pzsR2vefkG2XPBZpVq3a'
data_dict = {"FRED" : ["LF", "NA", "POP"], # Labor particiption, Employees on payroll, Population, takes state abbreviation after code
            "FRBNY" : ["HDC_STLOAN_", "HDC_CCARD_"], # student Loan Debt Balance Per Capita, Credit card debt  per capita, takes state abbreviation after code
            "NCES" : ["SCHOOLS_FRGRADS_"]}  # ??? freshman graduation rate Full state name after code


states = {
        'AK': 'Alaska',
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

def getData(db, pre, post, state_name = False, state_dict = states):
    df = pd.concat([quandl.get("{}{}{}{}{}".format(db, "/", pre, name.upper() if state_name else abv, post)).rename(columns = {"Amount" : name}) for abv, name in states.items()],
                   axis = 1) #data frame type needs to also be listed
    df.index = ["{}_{}{}".format(year, pre, post) for year in df.index.year]
    return df




def get_panel(db_dict):
    for pre, post in db_dict["pre_post"]:
        print (getData(db_dict["db"], pre, post, db_dict["state"]))
    #return pd.concat([getData(db_dict["db"], pre, post, db["state"]) for pre, post in db_dict["pre_post"]])


# for abv, name in states.items:
#     for data_suffix in data_suffixs[:1]:
#         df = quandl.get(data_prefix + "/" + abv + data_suffix)
#         df.ix[dt.datetime(2005, 1, 1) : dt.datetime(2015, 12, 31)]
#         print(abv)
#         print(df.index)
