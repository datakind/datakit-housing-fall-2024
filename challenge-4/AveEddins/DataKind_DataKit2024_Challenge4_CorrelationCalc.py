import warnings
warnings.simplefilter(action='ignore')
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import matplotlib.pyplot as plt

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
    # Income should be positive
    if ('Income' in column):
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

# Find which measures most correlate with these 3 measures of interest in the
# most prone areas
for column in [femaBuilding, femaPopulation, doeEnergy]:
    print('----Correlation with', column, '----')
    print('\n')
    print('Focus areas')
    print(focusCountiesCA_DF.corrwith(focusCountiesCA_DF[column]).nlargest(5)) 
    print('\n')
    print('All counties (a check to see if correlation on smaller set affects outcome)')
    print(CA_DF.corrwith(CA_DF[column]).nlargest(5))
    print('\n')