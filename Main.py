import SeventyFiveF.ReadByFilter as Read
import os
import json
import pandas as pd

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

float_pattern = r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
pd.set_option("display.max_columns", None)                                      # Show all the columns
pd.set_option("display.max_rows", None)                                         # Show all the rows

def get_df(query_string):
    reader = Read.ReadByFilter(username, password, subscriptionKey, query_string)
    result = reader.post()
    df = pd.DataFrame(result["rows"])                                           # Import into a data frame
    return df

siteId_df = get_df("building and equip")       # Returns all buildings w/ siteId

siteId_List = siteId_df["siteRef"].tolist()
dis_List = siteId_df["dis"].tolist()

first = True
counter = 0
for site,name in zip(siteId_List, dis_List):
    try:
        name_string = name.split("-")[0]
        siteId = site.split(":")[1]
        # query_string = f"ccu and siteRef==@{siteId}"          # Retrieve all the CCUs at a site
        query_string = f"temp and space and not cm and siteRef==@{siteId}"
        print(f"{counter} {name_string}")

        # convert string pattern into number
        ccus = get_df(query_string)
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
            show_columns.to_csv("data.csv", header=True, index=False)
        else:
            show_columns.to_csv("data.csv", mode='a', header=False, index=False)
        counter += 1
    except Exception as e:
        print(f"Exception: {e}")








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