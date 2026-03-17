import os
from datetime import datetime, timedelta, date
import pandas as pd
import Tools.SeventyFiveF_API as ApiTools
import Tools.TextTools as TextTools
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import SeventyFiveF.hisReadMany as rm
import Tools.DataFrameTools as DataFrameTools
import calendar
from pathlib import Path
import numpy as np

"""
Read in the required data and determine how many hours per day a given zone is occupied between a given start date
and end date.
"""

start_date_string = "2026-02-01"
stop_date_string = "2026-02-28"

# Returns 15 minute increments
def add_months(dt, months=1):
    year = dt.year + (dt.month - 1 + months) // 12
    month = (dt.month - 1 + months) % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)

def process_records():
# API Access Information
    username = os.environ.get("75F API Username")
    password = os.environ.get("75F API Password")
    subscriptionKey = os.environ.get("75F API Subscription Key")
    site_id = "20a474cf-1eb8-405b-af54-6a5d059dafcf"
    filter_tags = "mode,occupied"
    filter_string = f"mode and occupied and siteRef==@{site_id}"
    target_trend_domain_names = ['occupancyMode']

    # Instantiate tools classes
    api_tools = ApiTools.SeventyFiveF_API(username, password, subscriptionKey)
    text_tools = TextTools.TextTools()
    df_tools = DataFrameTools.DataFrameTools()

    # Get "Occupied Mode" trend ids
    occupied_mode_ids_df = api_tools.get_df_by_filter(filter_string)
    occupied_mode_ids_df.to_csv("_1_occupied_mode_ids_df.csv")
    occupied_mode_ids_df["id_ref"] = [text_tools.remove_type_information_text(x) for x in occupied_mode_ids_df["id"]]
    id_list = occupied_mode_ids_df["id_ref"].tolist()
    count = 0
    for id_item in id_list:

        # Configure Date Objects
        date_format_string="%Y-%m-%d"
        start_date = datetime.strptime(start_date_string, date_format_string).date()
        end_date = start_date
        #end_date = add_months(start_date, 1)
        #end_date = end_date + timedelta(days=-1)
        stop_date = datetime.strptime(stop_date_string, date_format_string).date()
        date_range = f"{start_date.strftime(date_format_string)},{end_date.strftime(date_format_string)}"

        ids = [id_item]
        count = count + 1

        # Get the historical data with hisReadMany
        results = ""
        trend_df = pd.DataFrame()
        while start_date < stop_date:
            print(f"({count} : {len(id_list)}) Processing date range: {date_range} for {id_item}")
            try:
                reader = rm.hisReadMany(username, password, subscriptionKey, ids, date_range)
                results = reader.post()
            except Exception as e:
                print(e)
            historical_df = pd.DataFrame(results["rows"])
            for row in historical_df.iterrows():
                new_df =  pd.DataFrame(row[1]["data"])
                trend_df = pd.concat([trend_df, new_df], ignore_index=True)

            start_date = start_date + timedelta(days=1)
            # start_date = add_months(start_date, 1)
            end_date = start_date#  + timedelta(days=1)
            # end_date = add_months(start_date, 1)
            # end_date = end_date + timedelta(days=-1)
            date_range = f"{start_date.strftime(date_format_string)},{end_date.strftime(date_format_string)}"

        trend_df.insert(0, "id", id_item)
        trend_df.to_csv(f"data\\{id_item}.csv", header=True, index=False)
        # break

# process_records()

def build_dataframe():
    directory = Path("C://Users//pknal//PycharmProjects//75F API Hello World//PayloadScripts//data")

    files = [f for f in directory.iterdir() if f.is_file()]

    count = 0
    first = True
    dft = DataFrameTools.DataFrameTools()

    date_index = pd.date_range(start=start_date_string, end=stop_date_string, freq="1min")
    results = pd.DataFrame()
    results["date"] = pd.NaT
    results["date"] = date_index
    results["date"] = pd.to_datetime(results["date"])
    results["date"] = results["date"].dt.tz_localize("UTC-05:00")
    # results.set_index(["date"], inplace=True)

    for file in files:
        try:
            count = count + 1
            print(file.name)
            df = pd.read_csv(f"data//{file.name}")
            df['val'] = df['val'].str.replace("n:", "", regex=False)
            dft.convert_ts_to_datetime_column(df, "ts", "date")
            dft.convert_val_to_numeric_value(df, "val", "value")
            df.replace(np.nan, 0, inplace=True)
            df["date"] = pd.to_datetime(df["date"])
            # df.set_index(["date"], inplace=True)

            results = results.merge(
                df[["date", "value"]],
                on="date",
                how="left"
            )
            new_name = file.name.replace(".csv", "")
            results = results.rename(columns={"value":new_name})
        except Exception as e:
            print(e)

        # mapping = df.set_index(["date"])["value"].to_dict()
        # results[file.name.replace(".csv", "")] = results.set_index(["date"]).index.map(mapping)

        # if count >= 1:
        #     break
        # else:
        #     count = count + 1

    results.fillna(0, inplace=True)
    results.to_csv("results.csv")
    print(results.shape)

process_records()
build_dataframe()

results = pd.read_csv("results.csv")
print(results.shape)

# numeric_cols = results.select_dtypes(include="number").columns
# df_filtered = results[results[numeric_cols] == 1].fillna(0)
# print(df_filtered)
results["date"] = pd.to_datetime(results["date"])
monthly_groups = results.groupby(results["date"].dt.to_period("M"))
print(monthly_groups)

count = 1
for month, group in results.groupby(results['date'].dt.to_period('M')):
    #print(month)
    group_df = pd.DataFrame(group)
    group_df.to_csv(f"payload//{month}_{count}.csv")
    count = count + 1


def process_group_1(group):
    minutes = 0
    for row in group.itertuples():
        if any(row):
            minutes = minutes + 1
    print(minutes / 60)

def process_group_2(group):
    minutes = 0
    for row in group.itertuples():
        true_count = sum(v==1 for v in row)
        avg_minutes = true_count / group.shape[1]
        minutes = minutes + avg_minutes
    print(minutes / 60)

print("Absolute Occupancy Hours")
results.groupby(results['date'].dt.to_period('M')).apply(process_group_1)

print("Average Occupancy Hours")
results.groupby(results['date'].dt.to_period('M')).apply(process_group_2)

