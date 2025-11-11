
# Read by filter (arrow operator): ver:"3.0" id,dis,equip,siteRef,system @6d78f1c0-d10a-4482-8058-db328441a669,"System Equip A",M,@b8a1a5be-3080-40e6-9161-64f39944db9e,M @84010772-46ec-4937-9430-71083196f2c4,"System Equip B",M,@b8a1a5be-3080-40e6-9161-64f39944db9e,M
# Read by filter with the arrow operator uses the same class as ReadByFilter.
# Not sure about the example given from the 75F API site above.
# Examples given in the page text (below) seem to work

import SeventyFiveF.ReadByFilter as Read
import os
import json

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

# Ready by id
siteRef = "@4f04cf8f-9d19-4138-b376-0cd468fc5545"
query_string = f"equipRef -> siteRef=={siteRef}"
reader = Read.ReadByFilter(username, password, subscriptionKey, query_string)
result = reader.post()

print(json.dumps(result, indent=4))  # Display the resulting dictionary in text



# Read by Filter - Arrow Operator (json)
# From: https://api-management-75f-dev.developer.azure-api.net/

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
# single - "equip and siteRef -> geoCity == \"Saint Paul\"". Translation: Find all equips at a site located in Saint Paul.

# siblings - "equip and siteRef -> geoCity == \"Saint Paul\"" and floorRef -> dis == \"Main\".
# Translation: Find all equips at a site located in Saint Paul and located on a floor named Main.

# boolean expression - "equip and ( siteRef -> geoCity == \"Saint Paul\"" or siteRef -> geoCity == \"Duluth\"" ).
# Translation: Find all equips at a site located in Saint Paul or Duluth

# Invalid Examples
# nested - "point and equipRef -> siteRef -> geoCity == \"Saint Paul\"").
# Translation: Find all points whose equip is at a site located in Saint Paul
