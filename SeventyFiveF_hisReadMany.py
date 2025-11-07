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

import requests
import SeventyFiveF_Auth
import json

def get_hisReadMany(username, password, subscription_key, ids, date_range):
    """
    Retrieves historical data from the 75F API using hisReadMany.
    Args:
        username (string):  The Facilisight username that has API privileges
        password (string):  The password for the above username
        subscription_key (string): The subscription key for the above username from the 75F API website
        ids (string): A line separated list of ids to retrieve historical data for (see README.md)
        date_range (string): The date range to pull historical data for

    Returns:
        results (json):

    """

    authorization_string = SeventyFiveF_Auth.get_authorization(username, password, subscription_key)

    url = "https://api.75f.io/haystack/hisReadMany"

    hdr ={
        'Authorization': authorization_string,
        'Accept': 'application/json',
        'Content-Type': 'text/zinc',
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # The list sent to the 75F API (ids) must consist of one id on each line without any leading or trailing spaces.
    # TODO: send in a CSV list and separate here to clean up the code
    data = \
f"""ver:\"3.0\" range:\"{date_range}\"
id
{ids}"""

    try:
        response = requests.post(url, data=data, headers=hdr, timeout=30)
        return json.loads(response.text)

    except Exception as e:
        return "" # TODO: Handle or raise Exception as appropriate