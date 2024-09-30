import pandas as pd
import requests
import itertools
import json

#HUD API info and token access available here: https://www.huduser.gov/portal/datasets/il.html#faq_2024

def get_county_codes(api_token, state_abbr):
    """
    Fetches county codes for a given state using the HUD API.

    This function makes a GET request to the HUD API to retrieve a list of county codes
    for a specified state. The response is returned as a pandas DataFrame containing 
    the state_code, fips_code, county_name, town_name, and category.

    Parameters:
    -----------
    api_token : str
        The API token required for authorization to make the request.
    state_abbr : str
        The state abbreviation (e.g., 'FL' for Florida) to fetch the county codes for.

    Returns:
    --------
    pd.DataFrame
        A pandas DataFrame containing the county data if the request is successful.
        The DataFrame includes county names and FIPS codes.
    
    None
        If the request fails (non-200 response), the function prints an error message
        and returns None.
    """
    hud_county_endpoint = f"https://www.huduser.gov/hudapi/public/fmr/listCounties/{state_abbr}"
    headers = {
    "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(hud_county_endpoint, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve counties with response code {response.status_code}.")
        return
    else:
        df_counties = pd.DataFrame(response.json())
        return df_counties


def get_county_il_data(api_token, df_counties):
    """
    Fetches income limit data for counties using the HUD API.

    This function makes a GET request to the HUD API for each county in the given
    DataFrame, identified by its FIPS code, to retrieve income limit data. It returns the results in 
    a pandas DataFrame with a column for the FIPS code, county name, and income 
    limits for each income and household size category.

    Parameters:
    -----------
    api_token : str
        The API token required for authorization to make the request.
    df_counties : pd.DataFrame
        The DataFrame from get_county_codes.

    Returns:
    --------
    pd.DataFrame
        A DataFrame containing the FIPS code, county name, and income limit data 
        for each county, with income limit data structured as keys like 
        'extremely_low-il30_p1', 'very_low-il30_p1', etc.

    Notes:
    The function prints an error message if the request fails for a specific county.
    """
    headers = {
    "Authorization": f"Bearer {api_token}"
    }
    all_data = []
    for index, row in df_counties.iterrows():
        entity_id = row["fips_code"]
        county_name = row["county_name"]
        # API call for each county using the fips_code (entity_id)
        hud_endpoint = f"https://www.huduser.gov/hudapi/public/il/data/{entity_id}"
        response = requests.get(hud_endpoint, headers=headers)
        if response.status_code == 200:
            data = response.json()["data"]
            # Initialize a dictionary for this row (county)
            row_data = {
                "fips_code": entity_id,
                "county_name": county_name
            }
            # Add data from il categories
            for category in ["extremely_low", "very_low", "low"]:
                if category in data:
                    for key, value in data[category].items():
                        # Append the category name to the il hh size and add to row_data
                        new_key = f"{category}-{key}"
                        row_data[new_key] = value
            # Append this row's data to the list
            all_data.append(row_data)
        else:
            print(f"Failed to retrieve data for entity_id {entity_id} with response code {response.status_code}")
    return pd.DataFrame(all_data)