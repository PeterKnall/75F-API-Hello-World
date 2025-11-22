import Tools.SeventyFiveF_API as api_tools
import Tools.TextTools as TextTools
import os
import pandas as pd

"""
Example 04
Retrieve the current time zones from equipment.  Some (not all) time zones affect the date stamp that the trend graphs
appear in.  

"""

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

tools = api_tools.SeventyFiveF_API(username, password, subscriptionKey)
text_tools = TextTools.TextTools()

site_ref_df = tools.get_all_site_ids_df()

site_ref_List = site_ref_df["siteRef"].tolist()                                 # copy siteRef's to List
dis_List = site_ref_df["dis"].tolist()                                          # copy display names to List

is_first = True
number_of_sites_processed = 0

final_time_zone_df = pd.DataFrame()

for site_ref,name in zip(site_ref_List, dis_List):
    name_string = text_tools.remove_building_equip_text(name)
    site_id = text_tools.remove_type_information_text(site_ref)
    siteId = text_tools.remove_type_information_text(site_ref)

    query_string = f"tz and not point and siteRef==@{site_id}"
    print(f"{number_of_sites_processed} {name}")

    time_zone_df = tools.get_df_by_filter(query_string)

    # Guard Clause: An exception is generated if the dataframe does not contain the expected columns.
    # Check for this situation so an exception handler is not necessary.
    if not  {'tz', 'dis'}.issubset(time_zone_df.columns):
        print(f"{name_string} Missing required columns - SKIP!.")
        time_zone_df.to_csv(f"_Error {name_string}.csv", header=True, index=False)
        continue

    filter_rows = ['dis', 'tz']
    filtered_time_zone_df = time_zone_df[filter_rows]

    # Append new value to report
    final_time_zone_df = pd.concat([final_time_zone_df, filtered_time_zone_df], ignore_index=True)

    if is_first:
        is_first = False
        time_zone_df.to_csv("time_zone_df.csv", header=True, index=False)
    else:
        time_zone_df.to_csv("time_zone_df.csv", header=True, index=False, mode='a')

    number_of_sites_processed += 1

print(final_time_zone_df)
final_time_zone_df.to_csv("final_time_zone_df.csv", header=True, index=False)