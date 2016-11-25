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

YEARS = (('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'),
        ('2004', '2004'), ('2005', '2005'), ('2006', '2006'), ('2007', '2007'), ('2008', '2008'),
        ('2009', '2009'), ('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'),
        ('2014', '2014'), ('2015', '2015'), ('2016', '2016'))
DATA = (('None', ''),
        ('HDC_CCARD_', "Household Credit Card Debt"),
        ('HDC_STLOAN', 'Household Student Loan Credit Card Deby'),
        ('LF', 'Civilian Labor Force'),
        ('NA','Non-Farm Employees'),
        ('POP', 'Population'),
        ('SCHOOLS_FGRADS', 'Average Freshman Graduation Rate'))


STATES_DICT = dict(STATES)
YEARS_DICT = dict(YEARS)
DATA_DICT = dict(DATA)

class Input(models.Model):
    state1 = models.CharField(max_length = 50, choices = STATES)
    state2 = models.CharField(max_length = 50, choices = STATES)
    state3 = models.CharField(max_length = 50, choices = STATES)
    #year = models.CharField(max_length = 4, choices = YEARS)
    data1 = models.CharField(max_length = 20, choices = DATA)
    data2 = models.CharField(max_length = 20, choices = DATA)
    data3 = models.CharField(max_length = 20, choices = DATA)

    name  = models.CharField(max_length=50)
