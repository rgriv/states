from django.db import models

STATES = (
    ('None', 'None'),
    ('AK', 'Alaska'),
    ('AL', 'Alabama'),
    ('AR', 'Arkansas'),
    ('AZ', 'Arizona'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('IA', 'Iowa'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('MA', 'Massachusetts'),
    ('MD', 'Maryland'),
    ('ME', 'Maine'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MO', 'Missouri'),
    ('MS', 'Mississippi'),
    ('MT', 'Montana'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('NE', 'Nebraska'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NV', 'Nevada'),
    ('NY', 'New York'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VA', 'Virginia'),
    ('VT', 'Vermont'),
    ('WA', 'Washington'),
    ('WI', 'Wisconsin'),
    ('WV', 'West Virginia'),
    ('WY', 'Wyoming')
   )
   
STATEFP = (
    ('AL',1),
    ('AK',2),
    ('AZ',4),
    ('AR',5),
    ('CA',6),
    ('CO',8),
    ('CT',9),
    ('DE',10),
    ('DC',11),
    ('FL',12),
    ('GA',13),
    ('HI',15),
    ('ID',16),
    ('IL',17),
    ('IN',18),
    ('IA',19),
    ('KS',20),
    ('KY',21),
    ('LA',22),
    ('ME',23),
    ('MD',24),
    ('MA',25),
    ('MI',26),
    ('MN',27),
    ('MS',28),
    ('MO',29),
    ('MT',30),
    ('NE',31),
    ('NV',32),
    ('NH',33),
    ('NJ',34),
    ('NM',35),
    ('NY',36),
    ('NC',37),
    ('ND',38),
    ('OH',39),
    ('OK',40),
    ('OR',41),
    ('PA',42),
    ('RI',44),
    ('SC',45),
    ('SD',46),
    ('TN',47),
    ('TX',48),
    ('UT',49),
    ('VT',50),
    ('VA',51),
    ('WA',53),
    ('WV',54),
    ('WI',55),
    ('WY',56),
    ('AS',60),
    ('GU',66),
    ('MP',69),
    ('PR',72),
    ('UM',74),
    ('VI',78),
)

YEARS = ( ('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'),
        ('2004', '2004'), ('2005', '2005'), ('2006', '2006'), ('2007', '2007'), ('2008', '2008'),
        ('2009', '2009'), ('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'),
        ('2014', '2014'), ('2015', '2015'), ('2016', '2016') )

DATA = (
('None', 'None'),
('agemunge_persons-0-to-4-years', 'Population 0 - 4 Years Old'),
('agemunge_persons-18-to-64-years', 'Population 18 to 64 Years Old'),
('agemunge_persons-5-to-17-years', 'Population 18 to 64 Years Old'),
('agemunge_persons-65-years-and-over', 'Population 65+ Years Old'),

('gender_female', 'Female Population'),
('gender_male', 'Male Population'),
('latino_persons-not-of-hispanic-or-latino-origin', 'Non-Hispanic/Latin Population'),
('latino_persons-of-hispanic-or-latino-origin', 'Hispanic/Latin Population'),
('race_american-indian-and-alaska-native-alone', 'American Indian/Alaskan Native Population'),
('race_asian-alone', 'Asian Population'),
('race_black-or-african-american-alone', 'Black Population'),
('race_native-hawaiian-and-other-pacific-native-alone', 'Native Hawaiian/Other Pacific Native Population'),
('race_some-other-race-alone', 'Other Race Populations'),
('race_two-or-more-races', 'Two or More Races Population'),
('race_white-alone', 'White Population'),
('total_total-population', 'Total Population'),

('NCES_SCHOOLS_FRGRADS__all-racesethnicities-female', 'Female Average Freshman Graduation Rate'),
('NCES_SCHOOLS_FRGRADS__all-racesethnicities-male', 'Male Average Freshman Graduation Rate'),
('NCES_SCHOOLS_FRGRADS__all-racesethnicities-total', 'Total Average Freshman Graduation Rate'),
('NCES_SCHOOLS_FRGRADS__american-indianalaska-native-female', 'Female American Indian/Alaskan Native AFGR'),
('NCES_SCHOOLS_FRGRADS__american-indianalaska-native-male', 'Male American Indian/Alaskan Native AFGR'),
('NCES_SCHOOLS_FRGRADS__american-indianalaska-native-total', 'Total American Indian/Alaskan Native AFGR'),
('NCES_SCHOOLS_FRGRADS__asianpacific-islander-female', 'Female Asian Pacific Islander AFGR'),
('NCES_SCHOOLS_FRGRADS__asianpacific-islander-male', 'Male Asian Pacific Islander  AFGR'),
('NCES_SCHOOLS_FRGRADS__asianpacific-islander-total', 'Total Asian Pacific Islander  AFGR'),
('NCES_SCHOOLS_FRGRADS__black-female', 'Male Black AFGR'),
('NCES_SCHOOLS_FRGRADS__black-male', 'Female Black AFGR'),
('NCES_SCHOOLS_FRGRADS__black-total', 'Total Black AFGR'),
('NCES_SCHOOLS_FRGRADS__hispanic-female', 'Female Hispanic AFGR'),
('NCES_SCHOOLS_FRGRADS__hispanic-male', 'Male Hispanic AFGR'),
('NCES_SCHOOLS_FRGRADS__hispanic-total', 'Total Hispanic AFGR'),
('NCES_SCHOOLS_FRGRADS__white-female', 'Female White AFGR'),
('NCES_SCHOOLS_FRGRADS__white-male', 'Male White AFGR'),
('NCES_SCHOOLS_FRGRADS__white-total', 'Total White AFGR'),

('FRBNY__HDC_CCARD_','Credit Card Debt Balances Per Capita'),
('FRBNY__HDC_STLOAN_','Student Loan Debt Balance Per Capita'),

('FRED__LF','Civilian Labor Force (thousands)'),
('FRED__NA','All Non-Farm Employees (thousands)'),
('FRED__POP','Population (thousands)'),

('dn_Balance', 'Balance (State & Local per capita)'),
('dn_Education', 'Education (State & Local per capita)'),
('dn_General Government', 'General Goverment (State & Local per capita)'),
('dn_Gross Public Debt', 'Gross Public Debt (State & Local per capita)'),
('dn_Health Care', 'Health Care (State & Local per capita)'),
('dn_Interest', 'Interest (State & Local per capita)'),
('dn_Other Borrowing', 'Other Borrowing (State & Local per capita)'),
('dn_Other Spending', 'Other Spending (State & Local per capita)'),
('dn_Pensions', 'Pensions (State & Local per capita)'),
('dn_Protection', 'Protection (State & Local per capita)'),
('dn_Total Spending', 'Total (State & Local per capita)'),
('dn_Transportation', 'Transportation (State & Local per capita)'),
('dn_Welfare', 'Welfare (State & Local per capita)'),

('pn_Balance', 'Balance (State & Local percent GDP)'),
('pn_Education', 'Education (State & Local percent GDP)'),
('pn_General Government', 'General Government (State & Local percent GDP)'),
('pn_Gross Public Debt', 'Gross Public Debt (State & Local percent GDP)'),
('pn_Health Care', 'Health Care (State & Local percent GDP)'),
('pn_Interest', 'Interest (State & Local percent GDP)'),
('pn_Other Borrowing', 'Other Borrowing (State & Local percent GDP)'),
('pn_Other Spending', 'Other Spending (State & Local percent GDP)'),
('pn_Pensions', 'Pensions (State & Local percent GDP)'),
('pn_Protection', 'Protection (State & Local percent GDP)'),
('pn_Total Spending', 'Total (State & Local percent GDP)'),
('pn_Transportation', 'Transportation (State & Local percent GDP)'),
('pn_Welfare', 'Welfare (State & Local percent GDP)'),

('bn_Balance', 'Balance (State & Local in $ billion)'),
('bn_Education', 'Education (State & Local in $ billion)'),
('bn_General Government', 'General Government (State & Local in $ billion)'),
('bn_Gross Public Debt', 'Gross Public Debt (State & Local in $ billion)'),
('bn_Health Care', 'Health Care (State & Local in $ billion)'),
('bn_Interest', 'Interest (State & Local in $ billion)'),
('bn_Other Borrowing', 'Other Borrowing (State & Local in $ billion)'),
('bn_Other Spending', 'Other Spending (State & Local in $ billion)'),
('bn_Pensions', 'Pensions (State & Local in $ billion)'),
('bn_Protection', 'Protection (State & Local in $ billion)'),
('bn_Total Spending', 'Total (State & Local in $ billion)'),
('bn_Transportation', 'Transportation (State & Local in $ billion)'),
('bn_Welfare', 'Welfare (State & Local in $ billion)'))


DISPLAY_TYPES = ( ('plot', 'plot'),
                    ('corrmatrix', 'corrmatrix'),
                    ('corrplot', 'corrplot'),
                    ('table', 'table'),
                    ('map', 'map'))

INTERSECT_DATA = ( ('True', 'True'),
                    ('False', 'False') )


STATES_DICT = dict(STATES)
YEARS_DICT = dict(YEARS)
DATA_DICT = dict(DATA)
ID_DICT = dict(INTERSECT_DATA)
DT_DICT = dict(DISPLAY_TYPES)
STATEFP_DICT = dict(STATEFP)

class Input(models.Model):
    state1 = models.CharField(max_length = 50, choices = STATES)
    state2 = models.CharField(max_length = 50, choices = STATES)
    state3 = models.CharField(max_length = 50, choices = STATES)
    state4 = models.CharField(max_length = 50, choices = STATES)
    state5 = models.CharField(max_length = 50, choices = STATES)
    state6 = models.CharField(max_length = 50, choices = STATES)
    state7 = models.CharField(max_length = 50, choices = STATES)
    state8 = models.CharField(max_length = 50, choices = STATES)

    data1 = models.CharField(max_length = 50, choices = DATA)
    data2 = models.CharField(max_length = 50, choices = DATA)
    data3 = models.CharField(max_length = 50, choices = DATA)
    data4 = models.CharField(max_length = 50, choices = DATA)
    data5 = models.CharField(max_length = 50, choices = DATA)
    data6 = models.CharField(max_length = 50, choices = DATA)
    data7 = models.CharField(max_length = 50, choices = DATA)
    data8 = models.CharField(max_length = 50, choices = DATA)

    start_year = models.CharField(max_length = 50, choices = YEARS)
    end_year = models.CharField(max_length = 50, choices = YEARS)

    display_type = models.CharField(max_length = 50, choices = DISPLAY_TYPES)
    intersect_data = models.CharField(max_length = 50, choices = INTERSECT_DATA)
