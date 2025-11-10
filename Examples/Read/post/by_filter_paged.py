
# Read by filter (paged): ver:"3.0" size:25 page:3 filter "system and equip and siteRef==@b8a1a5be-3080-40e6-9161-64f39944db9e"

import SeventyFiveF.ReadByFilterPaged as Read
import os
import json

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

# Ready by id
siteRef = "@4f04cf8f-9d19-4138-b376-0cd468fc5545"
query_string = f"siteRef=={siteRef}"
page_size = "3"
page_number = "1"
reader = Read.Read_By_Filter_Paged(username, password, subscriptionKey, query_string, page_size, page_number)
result = reader.post()

print(json.dumps(result, indent=4))  # Display the resulting dictionary in text
