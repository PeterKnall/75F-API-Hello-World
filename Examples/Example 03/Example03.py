import Tools.SeventyFiveF_API as API
import Tools.TextTools as TextTools
import os
import pandas as pd

"""
Example 03
Retrieve the current temperatures, desired heating setpoint, and desired cooling setpoint from all zones and display 
along side the Site Name and Equipment Name.  
Pulling all the information across all the projects may be too much for the API to handle at once, so the requests 
are broken down by site.

Output files:

site_ref_df.csv             Table of site data returned while searching for all the accessable sites

Note:  Moved get_df() to Tools.SeventyFiveF_API.py
"""


# Calculate the zone temperature deviation
def calculate_temperature_deviation(current_temp, desired_heating_temp, desired_cooling_temp):
    if current_temp < desired_heating_temp < 999:
        return current_temp - desired_heating_temp
    elif desired_cooling_temp < current_temp < 999:
        return current_temp - desired_cooling_temp
    else:
        return 0

# These values are stored in the Windows Environmental Variables so they can be accessed during runtime
# rather than having them publicly viewable on GitHub.
username = os.environ.get("75F API Username")                                   # 75F Facilisite username
password = os.environ.get("75F API Password")                                   # 75F Facilisite password
subscriptionKey = os.environ.get("75F API Subscription Key")                    # API Key from 75F API Management portal

# Regular Expression (Regex) pattern to recognize floating point values surrounded by text.
# This code assumes there is only one numeric value in the text.
float_pattern = r'[+-]?(\d+(\.\d*)?|\.\d+)'

pd.set_option("display.max_columns", None)                                      # Show all the columns
pd.set_option("display.max_rows", None)                                         # Show all the rows
pd.options.mode.chained_assignment = None                                       # Silence a warning from Pandas

api_tools = API.SeventyFiveF_API(username, password, subscriptionKey)
text_tools = TextTools.TextTools()

site_ref_df = api_tools.get_all_site_ids_df()                                   # Returns all buildings w/ siteId
site_ref_df.to_csv("site_ref_df.csv", header=True, index=False)                 # Save DataFrame to CSV for viewing

site_ref_List = site_ref_df["siteRef"].tolist()                                 # copy siteRef's to List
dis_List = site_ref_df["dis"].tolist()                                          # copy display names to List

is_first = True
number_of_sites_processed = 0

final_temp_report_df = pd.DataFrame()                                           # create report df outside of main loop

for site_ref,name in zip(site_ref_List, dis_List):
    name_string = text_tools.remove_building_equip_text(name)
    siteId = text_tools.remove_type_infromation_text(site_ref)

    # Retrieves the current temperature, desired heating setpoint, and desired cooling setpoint
    query_string = f"temp and not cm and not ti and ((desired and (heating or cooling)) or space) and siteRef==@{siteId}"
    print(f"{number_of_sites_processed} {name_string}")

    #
    equip_df = pd.DataFrame()
    try:
        equip_df = api_tools.get_df_by_filter(query_string)
    except Exception as e:
        print(f"Exception while retrieving DataFrame from API: {e}")
        continue

    # Guard Clause: An exception is generated if the dataframe does not contain the expected columns.
    # Check for this situation so an exception handler is not necessary.
    if not  {'equipRef', 'domainName'}.issubset(equip_df.columns):
        print(f"{name_string} Missing required columns - SKIP!.")
        equip_df.to_csv(f"_Error {name_string}.csv", header=True, index=False)
        continue

    df_filtered = pd.DataFrame()    # the DataFrame must exist before adding a column to it

    # Add the equipment id
    df_filtered["equipRef"] = equip_df[equip_df["domainName"] == "currentTemp"]["equipRef"]
    df_filtered["equip_id"] = [text_tools.remove_type_infromation_text(x) for x in df_filtered["equipRef"]]             # List Comprehension

    # Add the display name
    for i, row in df_filtered.iterrows():
        # "None Found" occurs for zones that do not have this domainName (desiredTempHeating was a bad choice).
        df = equip_df[equip_df["domainName"] == "currentTemp"]
        match = df[df["equipRef"] == row["equipRef"]]
        if not match.empty:
            df_filtered.loc[i, "display_name"] = match.iloc[0]["dis"].rsplit("-", 1)[0]
        else:
            # Add something to prevent "None" values that crash type conversions
            df_filtered.loc[i, "display_name"] = "None Found"

    # Add all the "curVal" cells for the rows with the domain name "desiredTempHeating"
    for i, row in df_filtered.iterrows():
        df = equip_df[equip_df["domainName"] == "desiredTempHeating"]
        match = df[df["equipRef"] == row["equipRef"]]
        if not match.empty:
            df_filtered.loc[i, "desiredTempHeating"] = match.iloc[0]["curVal"]
        else:
            # Add something to prevent "None" values that crash type conversions
            df_filtered.loc[i, "desiredTempHeating"] = "999"
    df_filtered["desired_temp_heating"] = pd.to_numeric(df_filtered["desiredTempHeating"].str.extract(float_pattern)[0])

    # Add all the "curVal" cells for the rows with the domain name "currentTemp"
    for i, row in df_filtered.iterrows():
        df = equip_df[equip_df["domainName"] == "currentTemp"]
        match = df[df["equipRef"] == row["equipRef"]]
        if not match.empty:
            df_filtered.loc[i, 'currentTemp'] = match.iloc[0]['curVal']
        else:
            # Add something to prevent "None" values that crash type conversions
            df_filtered.loc[i, "currentTemp"] = "999"
    df_filtered["current_temp"] = pd.to_numeric(df_filtered["currentTemp"].str.extract(float_pattern)[0])

    # Add all the "curVal" cells for the rows with the domain name "desiredTempCooling"
    for i, row in df_filtered.iterrows():
        df = equip_df[equip_df["domainName"] == "desiredTempCooling"]
        match = df[df["equipRef"] == row["equipRef"]]
        if not match.empty:
            df_filtered.loc[i, 'desiredTempCooling'] = match.iloc[0]['curVal']
        else:
            # Add something to prevent "None" values that crash type conversions
            df_filtered.loc[i, "desiredTempCooling"] = "999"
    df_filtered["desired_temp_cooling"] = pd.to_numeric(df_filtered["desiredTempCooling"].str.extract(float_pattern)[0])

    # Calculate the zone temperature deviation
    df_filtered["temp_deviation"] = [calculate_temperature_deviation(x, y, z)
        for x, y, z in zip(df_filtered["current_temp"], df_filtered["desired_temp_heating"], df_filtered["desired_temp_cooling"])
    ]

    # Drop columns not used in report
    df_filtered.drop('equipRef', axis=1, inplace=True)
    df_filtered.drop('desiredTempHeating', axis=1, inplace=True)
    df_filtered.drop('currentTemp', axis=1, inplace=True)
    df_filtered.drop('desiredTempCooling', axis=1, inplace=True)

    # Append new value to report
    final_temp_report_df = pd.concat([final_temp_report_df, df_filtered], ignore_index=True)

    # When printing output to file, overwrite the file during the first iteration and append afterwards
    if is_first:
        is_first = False
        df_filtered.to_csv("df_filtered.csv", header=True, index=False)
        equip_df.to_csv("equip_df.csv", header=True, index=False)
    else:
        df_filtered.to_csv("df_filtered.csv", header=True, index=False, mode='a')
        equip_df.to_csv("equip_df.csv", header=True, index=False, mode='a')

    number_of_sites_processed += 1


print(final_temp_report_df)
final_temp_report_df.to_csv("final_temp_report_df.csv", header=True, index=False)