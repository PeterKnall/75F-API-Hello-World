
# Read by filter: ver:"3.0" filter "system and equip and siteRef==@b8a1a5be-3080-40e6-9161-64f39944db9e"
# Read by filter (paged): ver:"3.0" size:25 page:3 filter "system and equip and siteRef==@b8a1a5be-3080-40e6-9161-64f39944db9e"
# Read by filter (arrow operator): ver:"3.0" id,dis,equip,siteRef,system @6d78f1c0-d10a-4482-8058-db328441a669,"System Equip A",M,@b8a1a5be-3080-40e6-9161-64f39944db9e,M @84010772-46ec-4937-9430-71083196f2c4,"System Equip B",M,@b8a1a5be-3080-40e6-9161-64f39944db9e,M
# Read by id: ver:"3.0" id @6d78f1c0-d10a-4482-8058-db328441a669 @84010772-46ec-4937-9430-71083196f2c4

import SeventyFiveF_Read
import os

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

date_range = "today"

# Ready by id
this_id = "@52bdc021-71d3-4479-903e-0b0986a993ee"
result = SeventyFiveF_Read.read_by_id(username, password, subscriptionKey, this_id)
print(result)
