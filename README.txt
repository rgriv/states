Group Members:
Amani Abou Harb
Roman Rivera
Ryan Tang


In order to run our site you need to have the following installed: 

Pandas, geopandas, os, matplotlib, numpy, mpld3 

Project Purpose:
Our original purpose was to investigate the relationship between household debt (such as student loans and credit cards) and civilian non-aggricultural workforce participation.

Eventually, we decided to add in other outside sources of information, such as census data, education information, and state/local government finances to create a database for the purose of state investigation and research.

Currently the project exists as a way to compare disparate time-series data sets by being able to plot them over them and compare between states. Additionally it has the functionality to display correlation tables and heat maps.

Functionality:
Website users can choose up to 8 state and data choices, a start year and end year between 2000-2016, display types, and the choice to join data by union or by intersection. Some data sources, eg. census data, do not exist every year but only in available years. In these cases, intersecting data may be the most useful. You can click reset page to reset the page.

Display Types:
Plot - Plot longitudinal data up to 8 state and data choices.
Corr Matrix - Display correlation table of data and state combinations
Corr Plot - Display heat map plot colorizing the magnitude of correlation between data and state choices
Table - Display the raw data frame as-is

Data Sources:
Quandl
FRED(Federal Reserve Economic Data) - Civilian Labor Force, All Non-Farm Employees, Population
FRBNY (Federal Reserve Bank of New York) - Credit Card Debt Balances per Capita, Student Loan Debt Balance Per Capita
NCES (Nation Center for Education Statistics) - Freshman Graduation Rates by Ethnicity and Gender

Census
Race
Ethnicity
Gender 
Age Group

usgovernmentspending.com
For per capita, percent GDP, and in billion dollars, we have state + local spending breakdowns for education, general government, welfare, etc.