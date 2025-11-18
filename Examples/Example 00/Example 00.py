import SeventyFiveF.ReadByFilter as Read
import os
import pandas as pd

"""
Example 00 - because computers start counting at zero, not one.
A simple example to pull the Site IDs from all sites "username" has access to in 75F Facilisight.
"""

# These values are stored in the Windows Environmental Variables so they can be accessed during runtime
# rather than having them publicly viewable on GitHub.
username = os.environ.get("75F API Username")                                   # 75F Facilisite username
password = os.environ.get("75F API Password")                                   # 75F Facilisite password
subscriptionKey = os.environ.get("75F API Subscription Key")                    # API Key from 75F API Management portal

# Set to flags in Pandas so the DataFrames are not abridged when printed to console,
pd.set_option("display.max_columns", None)                                      # Pandas option to show all the columns
pd.set_option("display.max_rows", None)                                         # Pandas option to Show all the rows

def get_df(query_string):
    """
    Retrieves data from the 75F API and returns the data in a Pandas DataFrame.
    :param query_string: A Haystack Query to select the desired data.
    :return: A Pandas Dataframe with the data returned from the API.
    """
    reader = Read.ReadByFilter(username, password, subscriptionKey, query_string)
    result = reader.post()
    df = pd.DataFrame(result["rows"])                                           # Import into a Pandas DataFrame
    return df

df = get_df("building and equip")                                               # Returns all building level equipment
df.to_csv("df.csv", header=True, index=False)

# The display name entries contain "-buildingEquip".  Remove this from all "dis" entries in the DataFrame.
# However, Python does not know that the data in this column is a string, so the values are "cast" into a string
# data type with ".str".
df['dis'] = df['dis'].str.replace('-buildingEquip', '')

selected_columns=['siteRef','dis']
selected_siteId_df = df[selected_columns]
selected_siteId_df.to_csv("selected_siteId_df.csv", header=True, index=False)

print(selected_siteId_df)
print(f"Available columns: {list(df.columns)}")