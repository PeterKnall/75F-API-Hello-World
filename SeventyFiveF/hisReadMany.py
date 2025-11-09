# Simple script to retrieve a historical values from 75F Haystack

# A special thanks for the following supporters:
#
# Scott and Madhu from 75F.
#
# Permanently deleted user (5 Nov 2025):
# Link-1 : https://support.75f.io/hc/en-us/articles/5460179115923-HisReadMany-API?input_string=auth+and+hisreadmany+api+help
# Link-2 : https://support.75f.io/hc/en-us/articles/5460365803027-75F-API-s-Error-Returns?input_string=auth+and+hisreadmany+api+help
#
# This example was pulled from the 75F API website and written for Python 3.2.
# This example was executed in Python 3.10.11
# the "requests" library replaced the "urllibs" library, which I could not get to work.

# Examples of Data format (Note: "id" and the subsequent list of ids must be on their own line with no extra whitespace).
# date-time range: ver:"3.0" range:"2020-01-01T12:00:00-04:00 New_York,2020-01-03T00:00:00-04:00 New_York" id @d7180b62-f926-4d22-812f-ed18b5c91937 @e8791f69-167c-47a2-8f9e-f25dd899b418
# date range: ver:"3.0" range:"2020-01-01,2020-01-07" id @d7180b62-f926-4d22-812f-ed18b5c91937 @e8791f69-167c-47a2-8f9e-f25dd899b418
# date: ver:"3.0" range:"2020-01-01" id @d7180b62-f926-4d22-812f-ed18b5c91937 @e8791f69-167c-47a2-8f9e-f25dd899b418
# latest: ver:"3.0" range:"latest" id @d7180b62-f926-4d22-812f-ed18b5c91937 @e8791f69-167c-47a2-8f9e-f25dd899b418
# today: ver:"3.0" range:"today" id @d7180b62-f926-4d22-812f-ed18b5c91937 @e8791f69-167c-47a2-8f9e-f25dd899b418
# yesterday: ver:"3.0" range:"yesterday" id @d7180b62-f926-4d22-812f-ed18b5c91937 @e8791f69-167c-47a2-8f9e-f25dd899b418
#

import requests
import json
import SeventyFiveF.Auth as Auth

class hisReadMany:
    """
    Retrieves historical data from the 75F API using "POST hisReadMany".
    Args:
        username (string):  The Facilisight username that has API privileges
        password (string):  The password for the above username
        subscription_key (string): The subscription key for the above username from the 75F API website
        ids (string): A CSV list of ids to retrieve historical data for (see README.md)
        date_range (string): The date range to pull historical data for

    Returns:
        results (dict):
    """

    def __init__(self, username, password, subscription_key, ids, date_range):
        self.username = username
        self.password = password
        self.subscription_key = subscription_key
        self.ids = ids
        self.date_range = date_range

    def post(self):
        authorization_string = Auth.get_authorization(self.username, self.password, self.subscription_key)
        url = "https://api.75f.io/haystack/hisReadMany"
        hdr ={
            'Authorization': authorization_string,
            'Accept': 'application/json',
            'Content-Type': 'text/zinc',
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': self.subscription_key,
        }
        # The list sent to the 75F API (ids) must consist of one id on each line without any leading or trailing spaces.
        item_list = self.ids.split(",")
        items = '\n'.join(item_list)
        data = f"ver:\"3.0\" range:\"{self.date_range}\"\nid\n{items}"
        try:
            response = requests.post(url, data=data, headers=hdr, timeout=30)
            return json.loads(response.text)
        except Exception as e:
            raise Exception(f"Exception during SeventyFiveF.hisReadMany.post(): {e}")