import SeventyFiveF.ReadByFilter as Read
import os
import json
import pandas as pd

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

site_ids = []
site_ids.append(("Canal Park Stadium", "20a474cf-1eb8-405b-af54-6a5d059dafcf"))
site_ids.append(("MSC1", "3c51ac7c-2cb7-429b-bafc-f5d6e879038a"))

def get_time_zones(item_string):
    # print(item_string)
    query_string = f"equipRef -> siteRef==@{item_string[1]}"
    # print(query_string)
    reader = Read.ReadByFilter(username, password, subscriptionKey, query_string)
    result = reader.post()

    pd.set_option("display.max_columns", None)                                      # Show all the columns
    pd.set_option("display.max_rows", None)
    df = pd.DataFrame(result["rows"])                                               # Import into a data frame

    tz_set = set(df["tz"])
    print(f"{item_string[0]} : {tz_set}")

for item in site_ids:
    get_time_zones(item)


# An arrow operator allows a filter to search one level deeper, effectively combining what would be two API calls into
# one. For example, it is possible to search for all equips located at a site in Saint Paul with one API call. If entity
# 1 points to entity 2 via a ref tag, then the arrow operator will evaluate a condition against entity 2. The left hand
# side (LHS) of the arrow operator points to another entity's id, via a ref. The matching entity is then evaluated by
# the condition on the right hand side (RHS) of the arrow operator.

# Requirements
# One or many separate arrow operators at the same level (i.e. siblings) are allowed. See example below.

# An arrow operator that points to another arrow operator (i.e. nested) is NOT allowed. Searching two levels deep is
# not allowed. See example below.

# An arrow operator can be joined within boolean expressions. See example below.

# The LHS of the arrow operator must be a ref tag name (e.g. siteRef).

# The RHS of the arrow operator is a standard filter condition.

# Examples
# single - "equip and siteRef -> geoCity == \"Saint Paul\"".
# Translation: Find all equips at a site located in Saint Paul.

# siblings - "equip and siteRef -> geoCity == \"Saint Paul\"" and floorRef -> dis == \"Main\".
# Translation: Find all equips at a site located in Saint Paul and located on a floor named Main.

# boolean expression - "equip and ( siteRef -> geoCity == \"Saint Paul\"" or siteRef -> geoCity == \"Duluth\"" ).
# Translation: Find all equips at a site located in Saint Paul or Duluth

# Invalid Examples
# nested - "point and equipRef -> siteRef -> geoCity == \"Saint Paul\"").
# Translation: Find all points whose equip is at a site located in Saint Paul