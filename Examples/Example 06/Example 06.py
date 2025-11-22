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
from a single zone and plot them.
"""

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

float_pattern = r'[+-]?(\d+(\.\d*)?|\.\d+)'

tools = api_tools.SeventyFiveF_API(username, password, subscriptionKey)
text_tools = TextTools.TextTools()

# x-axis display option for matplotlib.pyplot to show the date information in hours and minutes
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# Reservoir Park Second Floor VAV 16
room_ref = "5fd12b52-b7b6-43b7-b958-1d74d9912c92"
target_trend_domain_names = ['currentTemp', 'desiredTempCooling', 'desiredTempHeating']

# Build hisReadMany query string based on the domain names selected above
is_first = True
query_string = f"roomRef==@{room_ref} and ("
for domain_name in target_trend_domain_names:
    if is_first:
        is_first = False
    else:
        query_string = query_string + " or "
    query_string = query_string + f"domainName==@{domain_name}"
query_string = query_string + ")"

# Retrieve a data frame containing the necessary IDs
point_ref_df = pd.DataFrame()
try:
    point_ref_df = tools.get_df_by_filter(query_string)
except Exception as e:
    print(f"Exception while retrieving DataFrame from API: {e}\nQuery string:\n{query_string}")
point_ref_df.to_csv("point_ref_df.csv", header=True, index=False)

# Convert ids to a comma separated string to send to rm.hisReadMany
point_ref_df["idRef"] = [text_tools.remove_type_information_text(x) for x in point_ref_df["id"]]
point_ref_df["idRef"] = point_ref_df["idRef"].astype(str)
ids = point_ref_df["idRef"].tolist()

# Get the historical data with hisReadMany
date_range = "today"
results = ""
try:
    reader = rm.hisReadMany(username, password, subscriptionKey, ids, date_range)
    results = reader.post()
except Exception as e:
    print(e)
historical_df = pd.DataFrame(results["rows"])
historical_df.to_csv("historical_df.csv", header=True, index=False)

# For each trend returned, add it to a plot
for row in historical_df.iterrows():
    trend_df = pd.DataFrame(row[1]["data"])
    trend_df.to_csv("trend_df.csv", header=True, index=False)

    # Wrangle the date stamp
    trend_df['date_value1'] = trend_df['ts'].str.split(":", n=1).str[1]             # Remove the "n:" portion of the date stamp
    trend_df['date_value2'] = trend_df['date_value1'].str.split(" ", n=1).str[0]    # Remove the city portion of the date stamp (Detroit)
    trend_df['time'] = pd.to_datetime(trend_df['date_value2'], format="ISO8601")    # Convert to datetime object

    # Convert curVal to a float type
    trend_df["value"] = pd.to_numeric(trend_df["val"].str.extract(float_pattern)[0])

    # Remove unneeded columns / clean-up df
    trend_df = trend_df.drop("val", axis=1)
    trend_df = trend_df.drop("ts", axis=1)
    trend_df = trend_df.drop("date_value1", axis=1)
    trend_df.drop("date_value2", axis=1, inplace=True)

    # Add this Dataframe's information to the current plot, but do not show the plot yet
    plt.plot(trend_df['time'], trend_df['value'], label=row[1]["domainName"])

plt.show()                                                                          # Show the plot