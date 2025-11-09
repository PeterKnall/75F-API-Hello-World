"""
A simple example of the 75F's API for hisReadMany using POST that displays the resulting "dict" object
for the last (latest) trend point identified
"""
import os
import json
import SeventyFiveF.hisReadMany as rm

# Request "data" format - Replace spaces after "range" with newline characters "\n"
#
# date-time range: ver:"3.0" range:"2020-01-01T12:00:00-04:00 New_York,2020-01-03T00:00:00-04:00 New_York" id @d7180b62-f926-4d22-812f-ed18b5c91937 @e8791f69-167c-47a2-8f9e-f25dd899b418

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

date_range = "2025-11-01T12:00:00-04:00 Detroit,2025-11-01T18:00:00-04:00 Detroit"
id = "@52bdc021-71d3-4479-903e-0b0986a993ee"

# POST Call to API.  Returns a dict object.
try:
    results = rm.post(username, password, subscriptionKey, id, date_range)
    print(json.dumps(results, indent=4))        # Display the resulting dictionary in text
except Exception as e:
    print(e)