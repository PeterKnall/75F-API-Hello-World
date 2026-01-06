import os
from datetime import datetime, timedelta
import pandas as pd
import Tools.SeventyFiveF_API as ApiTools
import Tools.TextTools as TextTools
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import SeventyFiveF.hisReadMany as rm
import Tools.DataFrameTools as DataFrameTools

"""
Read in the required data and determine how many hours per day a given zone is occupied between a given start date
and end date.
"""

# API Access Information
username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")
start_date_string = "2026-01-04"
end_date_string = "2026-01-05"
site_id = "20a474cf-1eb8-405b-af54-6a5d059dafcf"
filter_tags = "mode,occupied"
filter_string = f"mode and occupied and siteRef==@{site_id}"
target_trend_domain_names = ['occupancyMode']

# Instantiate tools classes
api_tools = ApiTools.SeventyFiveF_API(username, password, subscriptionKey)
text_tools = TextTools.TextTools()
df_tools = DataFrameTools.DataFrameTools()

# Configure Date Objects
date_format_string="%Y-%m-%d"
start_date = datetime.strptime(start_date_string, date_format_string).date()
end_date = start_date + timedelta(days=1)
stop_date = datetime.strptime(end_date_string, date_format_string).date()
date_range = f"{start_date.strftime(date_format_string)},{end_date.strftime(date_format_string)}"

# Get "Occupied Mode" trend ids
occupied_mode_ids_df = api_tools.get_df_by_filter(filter_string)
occupied_mode_ids_df.to_csv("_1_occupied_mode_ids_df.csv")
occupied_mode_ids_df["id_ref"] = [text_tools.remove_type_information_text(x) for x in occupied_mode_ids_df["id"]]

id_list = occupied_mode_ids_df["id_ref"].tolist()
print(id_list)

# Get the historical data with hisReadMany
results = ""
try:
    reader = rm.hisReadMany(username, password, subscriptionKey, id_list, date_range)
    results = reader.post()
except Exception as e:
    print(e)
historical_df = pd.DataFrame(results["rows"])
historical_df.to_csv("_2_historical_df.csv", header=True, index=False)

for row in historical_df.iterrows():
    trend_df = pd.DataFrame(row[1]["data"])
    print(trend_df.shape)
