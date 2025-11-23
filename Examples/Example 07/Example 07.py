import os
import pandas as pd
import Tools.SeventyFiveF_API as ApiTools
import Tools.TextTools as TextTools
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import SeventyFiveF.hisReadMany as rm
import Tools.DataFrameTools as DataFrameTools

"""
Example 07
Read in the current temperature, desired heating temperature, and desired cooling temperature historical values
from several zones and plot them.
"""

# API Access Information
username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

# Storage Location Information
parent_directory_name = "Pictures"
os.makedirs(parent_directory_name, exist_ok=True)
directory_date_format_pattern = "%Y-%m-%d"

# What am I doing?
target_trend_domain_names = ['currentTemp', 'desiredTempCooling', 'desiredTempHeating']
date_range = "yesterday"

# Instantiate tools classes
api_tools = ApiTools.SeventyFiveF_API(username, password, subscriptionKey)
text_tools = TextTools.TextTools()
df_tools = DataFrameTools.DataFrameTools()

try:
    # Get all Site Ids
    site_ref_df = api_tools.get_all_site_ids_df()
    site_ref_df.to_csv("site_ref_df.csv", header=True, index=False)
    site_ref_list = site_ref_df["siteRef"].tolist()
    dis_list = site_ref_df["dis"].tolist()

    for site_id, display_name in zip(site_ref_list, dis_list):
        name_string = text_tools.remove_building_equip_text(display_name)
        site_string = text_tools.remove_type_information_text(site_id)
        print(f"{display_name} {site_string} {'x'*10}")
        site_directory_name = f"{parent_directory_name}\\{name_string}"
        os.makedirs(site_directory_name, exist_ok=True)

        room_ref_df = api_tools.get_all_rooms_from_site_df(site_string)
        room_ref_df.to_csv("room_ref_df.csv", header=True, index=False)  # "id" is the roomRef
        room_ref_list = room_ref_df["id"].tolist()

        if not room_ref_list:
            print(f"Room list for {display_name} is empty - SKIP")
            continue

        for room_id in room_ref_list:

            # Generate Query String
            room_ref = text_tools.remove_type_information_text(room_id)
            query_string = text_tools.get_query_string("roomRef", room_ref, "domainName", target_trend_domain_names)

            # Retrieve a data frame containing the necessary IDs.  Catch any exceptions and skip entry.
            point_ref_df = pd.DataFrame()
            try:
                point_ref_df = api_tools.get_df_by_filter(query_string)
            except Exception as e:
                print(f"Exception while retrieving DataFrame from API: {e}\nQuery string:\n{query_string}")
                continue
            point_ref_df.to_csv("point_ref_df.csv", header=True, index=False)

            # Guard Clause: An exception is generated if the dataframe does not contain the expected columns.
            # Check for this situation so an exception handler is not necessary.
            if not {'id'}.issubset(point_ref_df.columns):
                print(f"{name_string} Missing required \'id\' column - SKIP!.")
                continue

            # Convert ids to a comma separated string to send to rm.hisReadMany
            point_ref_df["id_ref"] = [text_tools.remove_type_information_text(x) for x in point_ref_df["id"]]
            point_ref_df["id_ref"] = point_ref_df["id_ref"].astype(str)
            id_list = point_ref_df["id_ref"].tolist()

            # Get the historical data with hisReadMany
            results = ""
            try:
                reader = rm.hisReadMany(username, password, subscriptionKey, id_list, date_range)
                results = reader.post()
            except Exception as e:
                print(e)
            historical_df = pd.DataFrame(results["rows"])
            historical_df.to_csv("historical_df.csv", header=True, index=False)

            # For each trend returned, add it to a plot
            # fig, ax = plt.subplots()
            date_directory = ""
            for row in historical_df.iterrows():
                trend_df = pd.DataFrame(row[1]["data"])
                trend_df.to_csv("trend_df.csv", header=True, index=False)

                # Guard Clause: An exception is generated if the dataframe does not contain the expected columns.
                # Check for this situation so an exception handler is not necessary.
                if not {'ts','val'}.issubset(trend_df.columns):
                    print(f"{name_string} Missing required columns \'ts\' or \'val\' - SKIP!.")
                    continue

                # Wrangle the date stamp
                try:
                    trend_df = df_tools.convert_ts_to_datetime_column(trend_df, "ts", "time")
                except Exception as e:
                    print(f"Exception while converting DateTime - SKIP: {e}")
                    continue

                trend_df = df_tools.convert_val_to_numeric_value(trend_df, "val", "value")

                trend_date = trend_df["time"].tolist()[1]
                trend_date_string = f"{trend_date.year}-{trend_date.month}-{trend_date.day}"

                # Add this Dataframe's information to the current plot, but do not show the plot yet
                plt.plot(trend_df['time'], trend_df['value'], label=row[1]["domainName"])
                date_directory = f"{site_directory_name}\\{trend_date_string}"

            title_string = point_ref_df["dis"].tolist()[0].split("-")[2]
            plt.title(title_string)                             # Add a title
            plt.ylim(top=85)
            plt.ylim(bottom=55)
            plt.xticks(fontsize=8, fontfamily='serif', rotation=45, fontweight='bold', color='black')
            plt.yticks(fontsize=8, fontfamily='serif', rotation=0, fontweight='bold', color='black')
            plt.grid(True)

            # x-axis display option for matplotlib.pyplot to show the date information in hours and minutes
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

            plt_filename = f"{date_directory}\\{name_string}_{title_string}.jpeg"
            try:
                os.makedirs(date_directory, exist_ok=True)
                plt.savefig(plt_filename)       # Safe to file
            except Exception as e:
                print(f"Exception while trying to save data to file - {plt_filename}: {e}")
            #plt.show()
            plt.clf()

            print(name_string, title_string)
            break  # Only show one plot for this site
        break # Only one site
except Exception as e:
    print(e)