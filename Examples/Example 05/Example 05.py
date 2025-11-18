import os
import pandas as pd
import matplotlib.pyplot as plt
import SeventyFiveF.hisReadMany as rm

"""
Example 05
Read in a historical value and plot it.
"""

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

float_pattern = r'[+-]?(\d+(\.\d*)?|\.\d+)'
pd.set_option("display.max_columns", None)                                      # Show all the columns
pd.set_option("display.max_rows", None)                                         # Show all the rows

# Reservoir Park Second Floor VAV 16 Current Temp
ids = ["@52bdc021-71d3-4479-903e-0b0986a993ee"]
date_range = "today"

# POST Call to API.  Returns a dict object.
try:
    reader = rm.hisReadMany(username, password, subscriptionKey, ids, date_range)
    results = reader.post()

    these_rows = results["rows"][0]["data"]                                     # Navigate thorough the dict and find the Trend Data List
    trend_df = pd.DataFrame(these_rows)                                         # Store that list in a Pandas Data Frame

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