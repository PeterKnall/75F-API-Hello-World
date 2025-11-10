import SeventyFiveF.ReadByFilter as Read
import os
import json
import pandas as pd

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

# If you do not specify a site id, it will query all the sites you have access to
siteRef = "@944c7e72-2b10-4c75-af58-47261a4d8d69"                               # Reservoir Park CC
query_string = f"zone and space and temp and siteRef=={siteRef}"                # Test this in Site Explorer

reader = Read.Read_By_Filter(username, password, subscriptionKey, query_string)
result = reader.post()

# There are three groups of dicts returned in the JSON object
print("-"*20)
print(json.dumps(result["metadata"], indent=4))                                 # Pretty print the JSON object
print("-"*20)
print(json.dumps(result["cols"], indent=4))                                     # Pretty print the JSON object
print("-"*20)
print(json.dumps(result["rows"], indent=4))                                     # Pretty print the JSON object
print("-"*20)

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

pd.set_option("display.max_columns", None)                                      # Show all the columns
df = pd.DataFrame(result["rows"])                                               # Import into a data frame
subset_cols = ["curVal", "dis", "id", "ccuRef", "equipRef", "floorRef", "roomRef"]
df_subset = df[subset_cols]

print(df_subset)

oldStuff = """


# Need to reincorporate the data wrangling items

ids = "@52bdc021-71d3-4479-903e-0b0986a993ee,@52b2309a-10ec-4578-af76-8c1130c58044"

float_pattern = r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'

pd.set_option('display.max_columns', None)                  # Pandas option to display all columns (do not use "...")
these_rows = results["rows"][0]["data"]                     # Navigate thorough the dict and find the Trend Data List
df = pd.DataFrame(these_rows)                               # Store that list in a Pandas Data Frame

# Wrangle the data value
df['str_value'] = df['val'].str.extract(float_pattern)[0]   # Extract the "number" portion of the value columns
df['value'] = pd.to_numeric(df['str_value'])                # Convert the text "number" portion to a numeric type

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