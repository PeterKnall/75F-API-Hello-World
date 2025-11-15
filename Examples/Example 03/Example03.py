import SeventyFiveF.ReadByFilter as Read
import os
import json
import pandas as pd

"""
Example 03
Retrieve the current temperatures, desired heating setpoint, and desired cooling setpoint from all zones and display 
along side the Site Name and Equipment Name.  
Pulling all the information across all the projects may be too much for the API to handle at once, so the requests 
are broken down by site.

Output files:

site_ref_df.csv             Table of site data returned while searching for all the accessable sites

"""

# These values are stored in the Windows Environmental Variables so they can be accessed during runtime
# rather than having them publicly viewable on GitHub.
username = os.environ.get("75F API Username")                                   # 75F Facilisite username
password = os.environ.get("75F API Password")                                   # 75F Facilisite password
subscriptionKey = os.environ.get("75F API Subscription Key")                    # API Key from 75F API Management portal

# Regular Expression (Regex) pattern to recognize floating point values surrounded by text.
# This code assumes there is only one numeric value in the text.
float_pattern = r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'

pd.set_option("display.max_columns", None)                                      # Show all the columns
pd.set_option("display.max_rows", None)                                         # Show all the rows
pd.options.mode.chained_assignment = None                                       # Silence a warning from Pandas

def get_df(query_string):
    """
    Retrieves data from the 75F API and returns the data in a Pandas DataFrame.
    :param query_string: A Haystack Query to select the desired data.
    :return: A Pandas Dataframe with the data returned from the API.
    """
    reader = Read.ReadByFilter(username, password, subscriptionKey, query_string)
    result = reader.post()
    df = pd.DataFrame(result["rows"])                                           # Import into a data frame
    return df

siteId_df = get_df("building and equip")                                        # Returns all buildings w/ siteId

site_ref_df = get_df("building and equip")                                      # Returns all buildings w/ siteId
site_ref_df.to_csv("site_ref_df.csv", header=True, index=False)       # Save DataFrame to CSV for viewing

# Pull the list of Site Ids and Display Names fom the DataFrame.  These lists will be in the same order as they appear
# in the DataFrame, so items with the same index will correspond to the same entry.
site_ref_List = site_ref_df["siteRef"].tolist()
dis_List = site_ref_df["dis"].tolist()

is_first = True
number_of_sites_processed = 0

# Create an empty DataFame outside the scope of the for loop so the DataFrame persists after the loop is complete.
final_temp_report_df = pd.DataFrame()

for site_ref,name in zip(site_ref_List, dis_List):
    name_string = name.split("-")[0]
    siteId = site_ref.split(":")[1]

    # Retrieves the current temperature, desired heating setpoint, and desired cooling setpoint
    query_string = f"temp and not cm and not ti and ((desired and (heating or cooling)) or space) and siteRef==@{siteId}"
    print(f"{number_of_sites_processed} {name_string}")

    equip_df = pd.DataFrame()
    try:
        equip_df = get_df(query_string)
    except Exception as e:
        print(f"Exception while retrieving DataFrame from API: {e}")

    df_filtered = pd.DataFrame()
    df_filtered["equipRef"] = equip_df[equip_df["domainName"] == "currentTemp"]["equipRef"]
    df_filtered["domainName"] = equip_df[equip_df["equipRef"] == df_filtered["equipRef"]]["domainName"]
    print(f"df_filtered: {df_filtered}")

    break
    oldText = """
    ccus["value_string"] = ccus["curVal"].str.extract(float_pattern)[0]
    ccus["value"] = pd.to_numeric(ccus["value_string"])

    ccus["site_name"] = name_string
    ccus["counter"] = counter

    # PK Pretty Print
    select_columns = ["counter", "site_name", "dis", "value", "unit"]
    show_columns = ccus[select_columns]
    # print(show_columns)
    if first:
        first = False
        show_columns.to_csv("DataFrameToolsTest.csv", header=True, index=False)
    else:
        show_columns.to_csv("DataFrameToolsTest.csv", mode='a', header=False, index=False)
    counter += 1
    """








oldStuff = """


# Need to reincorporate the data wrangling items


these_rows = results["rows"][0]["data"]                     # Navigate thorough the dict and find the Trend Data List
df = pd.DataFrame(these_rows)                               # Store that list in a Pandas Data Frame

# Wrangle the date stamp
df['date_value1'] = df['ts'].str.split(":", n=1).str[1]     # Remove the "n:" portion of the date stamp
df['date_value2'] = df['date_value1'].str.split(" ", n=1).str[0]  # Remove the city portion of the date stamp (Detroit)
df['time'] = pd.to_datetime(df['date_value2'], format="ISO8601")  # Convert to datetime object

# Remove unneeded columns / clean-up df
df = df.drop("val", axis=1)
df = df.drop("str_value", axis = 1)
df = df.drop("ts", axis=1)
df = df.drop("date_value1", axis=1)
df = df.drop("date_value2", axis=1)

# print(df)

df.plot(x='time', y='value')
plt.show()
"""


# There are three groups of dicts returned in the JSON object
# print("-"*20)
# print(json.dumps(result["metadata"], indent=4))                                 # Pretty print the JSON object
# print("-"*20)
# print(json.dumps(result["cols"], indent=4))                                     # Pretty print the JSON object
# print("-"*20)
# print(json.dumps(result["rows"], indent=4))                                     # Pretty print the JSON object
# print("-"*20)

# What is returned in the "rows" section is data about the currentTemp points that satisfy the query above.
# Next, the interesting data needs to be pulled out and wrangled before being displayed in a graph.
# For this example, interesting data includes:
#    * id           "id": "r:9ce9946d-14e2-42ac-aa26-e68af9ac2a0d"
#    * curVal       "curVal": "n:63.2"
#    * dis          "dis": "Reservoir Park-VAV-1100-Current Temp"
#    * ccuRef       "ccuRef": "r:b0f9b93b-3045-4cc5-a899-f474054a502e"
#    * equipRef     "equipRef": "r:0845c5b9-8e78-4b14-960f-1a8212ec766e"
#    * floorRef     "floorRef": "r:ebcbfd07-f5a8-4029-ad2f-9d2336ee531a"
#    * roomRef      "roomRef": "r:dea5e0de-0787-4006-aa8c-51358afb99a5"
# The "Ref" values will allow the points to be group dynamically later on.  The other rows can deleted.