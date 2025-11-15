import SeventyFiveF.ReadByFilter as Read
import os
import pandas as pd

"""
Example 01
Retrieve all CCUs across all projects.  Pulling all the CCUs across all the projects may be too much for the API
to handle at once, so the requests are broken down by site.

Output files:

site_ref_df.csv             Table of site data returned while searching for all the accessable sites
site_ccu_df.csv             The CCU information returned on a per-site basis (appended together into one CSV)
final_ccu_df.csv            The final CCU table
"""

# These values are stored in the Windows Environmental Variables so they can be accessed during runtime
# rather than having them publicly viewable on GitHub.
username = os.environ.get("75F API Username")                                   # 75F Facilisite username
password = os.environ.get("75F API Password")                                   # 75F Facilisite password
subscriptionKey = os.environ.get("75F API Subscription Key")                    # API Key from 75F API Management portal

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

site_ref_df = get_df("building and equip")                                      # Returns all the site ids for all bldgs
site_ref_df.to_csv("site_ref_df.csv", header=True, index=False)       # Save DataFrame to CSV for viewing

# Pull the list of Site Ids and Display Names fom the DataFrame.  These lists will be in the same order as they appear
# in the DataFrame, so items with the same index will correspond to the same entry.
site_ref_List = site_ref_df["siteRef"].tolist()
dis_List = site_ref_df["dis"].tolist()

is_first = True
number_of_sites_processed = 0

# Create an empty DataFame outside the scope of the for loop so the DataFrame persists after the loop is complete.
final_ccu_df = pd.DataFrame()

# This is where we make the chimichangas
for site_ref,dis in zip(site_ref_List, dis_List):
    name_string = dis.split("-")[0]                         # Remove "-buildingEquip" from text
    site_id = site_ref.split(":")[1]                        # Remove "r:" from text
    print(f"{number_of_sites_processed} {name_string}")     # Let the user know you're working on it

    query_string = f"ccu and siteRef==@{site_id}"           # Retrieve all the CCUs at a site

    # Try/Except should only surround the code that may generate an exception
    try:
        site_ccu_df = get_df(query_string)
    except Exception as e:
        print(f"Exception: {e}")

    # Guard Clause: An exception is generated if the dataframe does not contain the expected columns.
    # Check for this situation so an exception handler is not necessary.
    if not {'dis', 'createdDate'}.issubset(site_ccu_df.columns):
        print(f"{name_string} CCU list is empty.")
        continue                                            # SKIP!

    # Overwrite the output file the first time, append afterwards
    if is_first:
        site_ccu_df.to_csv("site_ccu_df.csv", header=True, index=False)
        is_first = False
    else:
        site_ccu_df.to_csv("site_ccu_df.csv", header=False, index=False, mode='a')

    column_filter_list = ["dis", "createdDate"]
    filtered_ccu_df = site_ccu_df[column_filter_list]
    filtered_ccu_df['site_id'] = site_id
    filtered_ccu_df['site_name'] = name_string
    final_ccu_df = pd.concat([final_ccu_df, filtered_ccu_df], ignore_index=True)

    number_of_sites_processed += 1

# View the results
print(final_ccu_df)
final_ccu_df.to_csv("final_ccu_df.csv", header=True, index=False)