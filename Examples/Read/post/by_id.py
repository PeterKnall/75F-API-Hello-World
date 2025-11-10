
# Read by id: ver:"3.0" id @6d78f1c0-d10a-4482-8058-db328441a669 @84010772-46ec-4937-9430-71083196f2c4

import SeventyFiveF.ReadById as Read
import os
import json

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

# Ready by id
this_id = "@52bdc021-71d3-4479-903e-0b0986a993ee"
reader = Read.Read_By_Id(username, password, subscriptionKey, this_id)
result = reader.post()

print(json.dumps(result, indent=4))  # Display the resulting dictionary in text
