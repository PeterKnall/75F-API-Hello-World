import os
import pandas as pd
import Tools.SeventyFiveF_API as api_tools
import Tools.TextTools as TextTools
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import SeventyFiveF.hisReadMany as rm

"""
Example 06
Read in the current temperature, desired heating temperature, and desired cooling temperature historical values
and plot them.
"""

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

float_pattern = r'[+-]?(\d+(\.\d*)?|\.\d+)'
pd.set_option("display.max_columns", None)                                        # Show all the columns
pd.set_option("display.max_rows", None)                                           # Show all the rows

tools = api_tools.SeventyFiveF_API(username, password, subscriptionKey)
text_tools = TextTools.TextTools()

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# Reservoir Park Second Floor VAV 16 Current Temp
# Retrieve the necessary Ids
roomRef = "5fd12b52-b7b6-43b7-b958-1d74d9912c92"
target_trend_domain_names = ['currentTemp', 'desiredTempCooling', 'desiredTempHeating']

# Build hisReadMany query string based on domain names
is_first = True
query_string = f"roomRef==@{roomRef} and ("
for domain_name in target_trend_domain_names:
    if is_first:
        is_first = False
    else:
        query_string = query_string + " or "
    query_string = query_string + f"domainName==@{domain_name}"
query_string = query_string + ")"
# print(query_string)

# Retrieve a data frame containing the necessary IDs
point_ref_df = pd.DataFrame()
try:
    point_ref_df = tools.get_df_by_filter(query_string)
except Exception as e:
    print(f"Exception while retrieving DataFrame from API: {e}")
point_ref_df.to_csv("point_ref_df.csv", header=True, index=False)

# Convert ids to a comma separated string
point_ref_df["idRef"] = [text_tools.remove_type_infromation_text(x) for x in point_ref_df["id"]]
point_ref_df["idRef"] = "@" + point_ref_df["idRef"].astype(str)
id_list = point_ref_df["idRef"].tolist()
ids = ",".join(id_list)
# print(f"ids: {ids}")

# Get the historical data with hisReadMany
date_range = "today"
results = ""
try:
    reader = rm.hisReadMany(username, password, subscriptionKey, ids, date_range)
    results = reader.post()
    #print(json.dumps(results, indent=4))        # Display the resulting dictionary in text
except Exception as e:
    print(e)
historical_df = pd.DataFrame(results["rows"])
historical_df.to_csv("historical_df.csv", header=True, index=False)

# For each trend returned, add it to a plot
for row in historical_df.iterrows():
    trend_df = pd.DataFrame(row[1]["data"])
    trend_df.to_csv("trend_df.csv", header=True, index=False)

    # Wrangle the date stamp
    trend_df['date_value1'] = trend_df['ts'].str.split(":", n=1).str[1]           # Remove the "n:" portion of the date stamp
    trend_df['date_value2'] = trend_df['date_value1'].str.split(" ", n=1).str[0]  # Remove the city portion of the date stamp (Detroit)
    trend_df['time'] = pd.to_datetime(trend_df['date_value2'], format="ISO8601")  # Convert to datetime object

    # Convert curVal to a float type
    trend_df["value"] = pd.to_numeric(trend_df["val"].str.extract(float_pattern)[0])

    # Remove unneeded columns / clean-up df
    trend_df = trend_df.drop("val", axis=1)
    trend_df = trend_df.drop("ts", axis=1)
    trend_df = trend_df.drop("date_value1", axis=1)
    trend_df.drop("date_value2", axis=1, inplace=True)

    plt.plot(trend_df['time'], trend_df['value'], label=row[1]["domainName"])
plt.show()


'''
date_range = "today"

# turn target_trend_domain_names into a list of ids
for domain_name in target_trend_domain_names:
    pass
ids=[]

try:
    reader = rm.hisReadMany(username, password, subscriptionKey, ids, date_range)
    results = reader.post()

    these_rows = results["rows"][0]["data"]                                       # Navigate thorough the dict and find the Trend Data List
    trend_df = pd.DataFrame(these_rows)                                           # Store that list in a Pandas Data Frame

    # Wrangle the date stamp
    trend_df['date_value1'] = trend_df['ts'].str.split(":", n=1).str[1]           # Remove the "n:" portion of the date stamp
    trend_df['date_value2'] = trend_df['date_value1'].str.split(" ", n=1).str[0]  # Remove the city portion of the date stamp (Detroit)
    trend_df['time'] = pd.to_datetime(trend_df['date_value2'], format="ISO8601")  # Convert to datetime object

    # Convert curVal to a float type
    trend_df["value"] = pd.to_numeric(trend_df["val"].str.extract(float_pattern)[0])

    # Remove unneeded columns / clean-up df
    trend_df = trend_df.drop("val", axis=1)
    trend_df = trend_df.drop("ts", axis=1)
    trend_df = trend_df.drop("date_value1", axis=1)
    trend_df.drop("date_value2", axis=1, inplace=True)

    trend_df.to_csv("trends_df.csv", header=True, index=False)

    trend_df.plot(x='time', y='value')
    plt.show()

except Exception as e:
    print(f"Exception: {e}")
'''