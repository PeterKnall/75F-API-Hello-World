import SeventyFiveF.ReadByFilter as Read
import os
import pandas as pd

"""
Example 02
Retrieve the current temperatures from all zones and display along side the Site Name and Equipment Name.  Pulling all
the information across all the projects may be too much for the API to handle at once, so the requests are broken down 
by site.

Output files:

site_ref_df.csv             Table of site data returned while searching for all the accessable sites
equip_df.csv                Equipment information returned on a per-site bases appended in a CSV
filtered_equip_df.csv       Filtered information returned on a per-site bases appended in a CSV
final_room_temps_df.csv     Room temperature report.
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

site_ref_df = get_df("building and equip")                                      # Returns all buildings w/ siteId
site_ref_df.to_csv("site_ref_df.csv", header=True, index=False)       # Save DataFrame to CSV for viewing

# Pull the list of Site Ids and Display Names fom the DataFrame.  These lists will be in the same order as they appear
# in the DataFrame, so items with the same index will correspond to the same entry.
site_ref_List = site_ref_df["siteRef"].tolist()
dis_List = site_ref_df["dis"].tolist()

is_first = True
number_of_sites_processed = 0

# Create an empty DataFame outside the scope of the for loop so the DataFrame persists after the loop is complete.
final_room_temps_df = pd.DataFrame()

# Main processing loop
for site_ref,dis in zip(site_ref_List, dis_List):
    name_string = dis.split("-")[0]                         # Remove "-buildingEquip" from text
    site_id = site_ref.split(":")[1]                        # Remove "r:" from text
    print(f"{number_of_sites_processed} {name_string}")

    # Some experimentation was required using Site Explorer to arrive at this query string.  Start with "temp",
    # and then review the data to find items that do not belong, then test to find which query tags remove them.
    query_string = f"temp and space and not cm and not ti and siteRef==@{site_id}"

    equip_df = pd.DataFrame()
    try:
        equip_df = get_df(query_string)
    except Exception as e:
        print(f"Exception: {e}")

    # Guard Clause: An exception is generated if the dataframe does not contain the expected columns.
    # Check for this situation so an exception handler is not necessary.
    if not  {'curVal', 'dis', 'unit'}.issubset(equip_df.columns):
        print(f"{name_string} Missing required columns - SKIP!.")
        continue

    # The value appears as the string "n:71.3 °F" in the DataFrame.  Use regex to separate the numeric portion,
    # then cast to a numeric value (creating new columns in equip_df along the way).
    equip_df["value_string"] = equip_df["curVal"].str.extract(float_pattern)[0]         # I <3 Regex
    equip_df["value"] = pd.to_numeric(equip_df["value_string"])

    equip_df['site_id'] = site_id
    equip_df['site_name'] = name_string
    equip_df["counter"] = number_of_sites_processed

    # Convert the set to a list so that the values can be used for column selection (and that information is only
    # declared once).
    column_filter_list = ["counter", "site_name", "dis", "value", "unit"]
    filtered_equip_df = equip_df[column_filter_list]
    final_room_temps_df = pd.concat([final_room_temps_df, filtered_equip_df], ignore_index=True)

    # Overwrite the output file the first time, append afterwards
    if is_first:
        is_first = False
        equip_df.to_csv("equip_df.csv", header=True, index=False)
        filtered_equip_df.to_csv("filtered_equip_df.csv", header=True, index=False)
    else:
        filtered_equip_df.to_csv("filtered_equip_df.csv", mode='a', header=False, index=False)
        equip_df.to_csv("equip_df.csv", header=True, index=False, mode='a')

    number_of_sites_processed += 1

print(final_room_temps_df)
final_room_temps_df.to_csv("final_room_temps_df.csv", header=True, index=False)