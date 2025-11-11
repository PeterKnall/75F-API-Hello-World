
# Read by filter: ver:"3.0" filter "system and equip and siteRef==@b8a1a5be-3080-40e6-9161-64f39944db9e"

import SeventyFiveF.ReadByFilter as Read
import os
import json

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

# Ready by id
query_string = "siteRef==@4f04cf8f-9d19-4138-b376-0cd468fc5545"
reader = Read.ReadByFilter(username, password, subscriptionKey, query_string)
result = reader.post()

print(json.dumps(result, indent=4))  # Display the resulting dictionary in text
