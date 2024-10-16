import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import matplotlib.pyplot as plt
import scipy.stats as stats

# -------------Getting started------------- #

# Questions to answer
# Where are communities located that have higher vulnerability to natural disasters?
# Who is represented in those communities?
# What is the housing make-up of those communities?
# Analysis insights and questions: 
#    What surprised you from this analysis? 
#    What are some limitations of the analysis? 
#    What are ways to extend the work?

# Set paths for data where housing-data file in same directory as code
CA_1_Path = r'housing-data\CA\data_1-CA.csv'
CA_2_Path = r'housing-data\CA\data_2-CA.csv'
FL_Path = r'housing-data\FL\data_1-FL.csv'
CA_1_Dictionary_Path = r'housing-data\CA\data_dictionary_1-CA.csv'
CA_2_Dictionary_Path = r'housing-data\CA\data_dictionary_2-CA.csv'
FL_Dictionary_Path = r'housing-data\FL\data_dictionary_1-FL.csv'

# Read csv files into dataframes
CA_1_DF = pd.read_csv(CA_1_Path)
CA_2_DF = pd.read_csv(CA_2_Path)
FL_DF = pd.read_csv(FL_Path)
CA_1_Dictionary_DF = pd.read_csv(CA_1_Dictionary_Path)
CA_2_Dictionary_DF = pd.read_csv(CA_2_Dictionary_Path)
FL_Dictionary_DF = pd.read_csv(FL_Dictionary_Path)

# Make one dataframe for CA
CA_DF = CA_1_DF.merge(CA_2_DF, how = 'outer')

# Use the dictionary files to replace the obscure column names
columnNameReplace = {}
for column in CA_DF.columns:
    if (column in list(CA_1_Dictionary_DF['field_name'])):
        index = list(CA_1_Dictionary_DF['field_name']).index(column)
        columnNameReplace[column] = CA_1_Dictionary_DF['dk_column_name'].iloc[index]
    if (column in list(CA_2_Dictionary_DF['field_name'])):
        index = list(CA_2_Dictionary_DF['field_name']).index(column)
        columnNameReplace[column] = CA_2_Dictionary_DF['dk_column_name'].iloc[index]       
CA_DF = CA_DF.rename(columns=columnNameReplace)

# Since the geoids are unique to each row, use them as the indices
CA_DF.set_index('geoid', inplace = True)

# one-hot encode the non-numeric columns
CA_DF = pd.get_dummies(CA_DF)

# Check for reasonable values
for column in CA_DF.columns:
    # Based on investigating the percentage columns with describe, remove some bad values
    # in the percentage columns
    if ('Percentage' in column) or ('Percentile' in column):
        CA_DF[column] = CA_DF[column].apply(lambda x: None if x < 0 or x > 100 else x)
    # Gini index ranges from 0 to 1
    if ('Gini' in column):
        CA_DF[column] = CA_DF[column].apply(lambda x: None if x < 0 or x > 1 else x)
    # Monetary columns should be positive
    if ('Income' in column) or ('Cost' in column):
        CA_DF[column] = CA_DF[column].apply(lambda x: None if x < 0 else x)

# Three measures here of community vulnerability in CA:
femaBuilding = 'FEMA (2014-2021) - Expected building loss rate (Natural Hazards Risk Index)'
femaPopulation = 'FEMA (2014-2021) - Expected population loss rate (Natural Hazards Risk Index)'
doeEnergy = 'DOE (2018) - Energy burden (percentile)'
    
topTenBuildingLossGeoIDsCA = CA_DF.nlargest(10, femaBuilding)[[femaBuilding]]
topTenPopulationLossGeoIDsCA = CA_DF.nlargest(10, femaPopulation)[[femaPopulation]]
topTenEnergyBurdenGeoIDsCA = CA_DF.nlargest(10, doeEnergy)[[doeEnergy]]

buildingIDsCA = topTenBuildingLossGeoIDsCA.index
populationIDsCA = topTenBuildingLossGeoIDsCA.index
energyIDsCA = topTenEnergyBurdenGeoIDsCA.index

# Find geo IDs that appear in at least two of the top ten vulnerabilities list
matchesCA = []
for i in range(len(buildingIDsCA)):
    for j in range(len(populationIDsCA)):
        for k in range(len(energyIDsCA)):
            if buildingIDsCA[i] == populationIDsCA[j]:
                matchesCA.append(buildingIDsCA[i])
            if energyIDsCA[k] == populationIDsCA[j]:
                matchesCA.append(energyIDsCA[k])
            if energyIDsCA[k] == buildingIDsCA[i]:
                matchesCA.append(energyIDsCA[k])
# Remove duplicates
mostVulnerableCommunitiesGeoIDsCA = set(matchesCA)

# Dig into those areas specifically
focusCountiesCA_DF = CA_DF.loc[list(mostVulnerableCommunitiesGeoIDsCA)]

# Create plots showcasing demographics aggregate across these counties
percentagesRaces = focusCountiesCA_DF[['ACS - Population Percentage by Race (Two or More Races)',
'ACS - Population Percentage by Race (White alone)',
'ACS - Population Percentage by Race (Black or African American alone)',
'ACS - Population Percentage by Race (American Indian and Alaska Native alone)',
'ACS - Population Percentage by Race (Asian alone)',
'ACS - Population Percentage by Race (Native Hawaiian and Other Pacific Islander alone)',
'ACS - Population Percentage by Race (Some Other Race Alone)']]

percentagesRaces.rename(columns = {'ACS - Population Percentage by Race (Two or More Races)': 'Two or More Races', 
                              'ACS - Population Percentage by Race (White alone)': 'White alone', 
                              'ACS - Population Percentage by Race (Black or African American alone)': 'Black or African American alone', 
                              'ACS - Population Percentage by Race (American Indian and Alaska Native alone)': 'American Indian and Alaska Native alone', 
                              'ACS - Population Percentage by Race (Asian alone)': 'Asian alone', 
                              'ACS - Population Percentage by Race (Native Hawaiian and Other Pacific Islander alone)': 'Native Hawaiian and Other Pacific Islander alone', 
                              'ACS - Population Percentage by Race (Some Other Race Alone)': 'Some Other Race Alone'}, inplace = True)

plt.figure()
plt.pie(percentagesRaces.mean(), labels = percentagesRaces.columns, autopct='%.2f')
plt.title('Average percentage of race across vulnerable counties')

# Working age segment vs retirement age segment
percentagesAges = focusCountiesCA_DF[['ACS - Population Percentage by Age (16 years and older) - Estimate',
                                       'ACS - Population Percentage by Age (65 years and older) - Estimate']]

percentagesAges.rename(columns = {'ACS - Population Percentage by Age (16 years and older) - Estimate': '16+',
                                  'ACS - Population Percentage by Age (65 years and older) - Estimate': '65+'},
                       inplace = True)

plt.figure()
percentagesAges.mean().plot(kind = 'bar', stacked = True)
plt.ylabel('Mean percentage of population')
plt.title('Age distribution in vulnerable areas')

# Relevant housing metrics

medianIncomeAndCosts = focusCountiesCA_DF[['ACS - Median Household Income last 12 months (in 2022 Inflation-Adjusted Dollars) - Estimate',
                                           'ACS - Median Monthly Housing Cost (Occupied Housing Units) - Estimate']]

medianIncomeAndCosts['ACS - Median Household Income last 12 months (in 2022 Inflation-Adjusted Dollars) - Estimate'] = medianIncomeAndCosts['ACS - Median Household Income last 12 months (in 2022 Inflation-Adjusted Dollars) - Estimate'].div(12).round(2)

medianIncomeAndCosts.rename(columns = {'ACS - Median Household Income last 12 months (in 2022 Inflation-Adjusted Dollars) - Estimate': 'Median Household Income Monthly',
                                       'ACS - Median Monthly Housing Cost (Occupied Housing Units) - Estimate': 'Median Monthly Housing Cost'}, inplace = True)

plt.figure()
plt.title('Median household income/housing cost across vulnerable counties')
ax = medianIncomeAndCosts.mean().plot(kind = 'bar', rot = 0)
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    
# On average, housing costs aren't too high compared to monthly income, as they're less than
# a third (21%)

# Ways to extend the work?
# First step would be understanding the specific vulnerabilities per county

plt.figure()
CA_DF.loc[buildingIDsCA].groupby('county')[[femaBuilding]].mean().sort_values(femaBuilding, ascending = False).plot(kind = 'bar', legend = False)
plt.title('Expected building loss rate by vulnerable county')
plt.ylabel('FEMA expected building loss rate')

plt.figure()
CA_DF.loc[populationIDsCA].groupby('county')[[femaPopulation]].mean().sort_values(femaPopulation, ascending = False).plot(kind = 'bar', legend = False)
plt.title('Expected population loss rate by vulnerable county')
plt.ylabel('FEMA expected building loss rate')

plt.figure()
CA_DF.loc[energyIDsCA].groupby('county')[[doeEnergy]].mean().sort_values(doeEnergy, ascending = False).plot(kind = 'bar', legend = False)
plt.title('DOE energy burden by vulnerable county')
plt.ylabel('DOE energy burden')

# 37 is the scariest since it appears in all 3 top tens with a large expected population
# loss rate

# What county is this? Why is its score so high? (also note highest expected population loss
# rate in the set is .0305 for county 115)

# 31 is Kings County (https://www2.census.gov/geo/docs/reference/codes2020/cou/st06_ca_cou2020.txt)
# Dataset used below: https://resilience.climate.gov/datasets/FEMA::national-risk-index-counties/explore?location=36.075321%2C-119.815527%2C9.97

nationalRiskIndexSet = pd.read_excel('National_Risk_Index_Counties_7941314701041212117.xlsx')

# Remove columns pertaining to national disasters not in Kings county (> 95% null values)
columnsToRemove = [x for x in nationalRiskIndexSet.columns if ('Tsunami' in x) or ('Volcanic Activity' in x) or ('Avalanche' in x)]
nationalRiskIndexSet.drop(columnsToRemove, axis = 1, inplace = True)

nationalRiskIndexSet37 = nationalRiskIndexSet[nationalRiskIndexSet['County Name'] == 'Kings']
nationalRiskIndexSet37 = nationalRiskIndexSet37[nationalRiskIndexSet37['State Name'] == 'California']

# Based on the 'hazard type risk index rating' columns, the high risks for Kings county
# are heat wave and drought, focus on those
removeIfInColumn = ['Winter Weather', 'Wildfire', 'Tornado', 'Strong Wind', 'Riverine Flooding', 'Lightning', 'Landslide',
                    'Ice Storm', 'Hurricane', 'Hail', 'Earthquake', 'Cold Wave', 'Coastal Flooding']
columnsToRemove = [x for x in nationalRiskIndexSet37.columns for inColumn in removeIfInColumn if (inColumn in x)]
nationalRiskIndexSet37.drop(columnsToRemove, axis = 1, inplace = True)

# This county has very high social vulnerability, very low community resilience,
# and a relatively moderate national risk index

# What is considered in these ratings? What makes an area socially vulnerable? Etc
# Social vulnerability: https://hazards.fema.gov/nri/social-vulnerability
# Community resilience: https://hazards.fema.gov/nri/community-resilience

# Mitigation measures for heat and drought: https://www.fema.gov/flood-maps/products-tools/national-risk-index/resources#heat

# Why exactly is heat and drought an issue?
# "Thousands of Americans suffer from heat-related illnesses and deaths each year. 
# Drought and wildfires can also affect agriculture and cause severe damage to communities 
# and infrastructure."

# From https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/SVI_documentation_2020.html:
# "The degree to which a community exhibits certain social conditions, including high 
# poverty, low percentage of vehicle access, or crowded households, may affect that 
# community’s ability to prevent human suffering and financial loss in the event of 
# disaster. These factors describe a community’s social vulnerability."

# Check for povery-related factors from CA_DF
# Relevant columns: 
# ACS - Percentage Below Poverty Level (Poverty Status in the Past 12 Months) - Estimate
# ACS - Gini Index of Income Inequality - Estimate

# Percentage below poverty level mean across county: 14.5% (12.3% across whole set)
# Gini Index of Income Inequality: .43 (.42 across whole set)

# See higher than average population below poverty level in this county, though
# Gini index is about the same

# Keep working towards understanding factors contributing to this specific
# county's risk, which can hopefully in turn be used to inform heat/drought mitigation
# for similarly affected counties