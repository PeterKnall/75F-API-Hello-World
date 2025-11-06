# Simple script to retrieve a historical values from 75F Haystack

# A special thanks for the following supporters:
#
# Scott and Madhu from 75F.
#
# Permanently deleted user:
# Link-1 : https://support.75f.io/hc/en-us/articles/5460179115923-HisReadMany-API?input_string=auth+and+hisreadmany+api+help
# Link-2 : https://support.75f.io/hc/en-us/articles/5460365803027-75F-API-s-Error-Returns?input_string=auth+and+hisreadmany+api+help
#
# This example was pulled from the 75F API website and written for Python 3.2.
# This example was executed in Python 3.10.11
# the "requests" library replaced the "urllibs" library, which I could not get to work.

import requests
import SeventyFiveF_Auth
import json

def getHisReadMany(username, password, subscriptionKey, ids, range):
    """
    Retrieves historical data from the 75F API using hisReadMany.
    Args:
        username (string):  The Facilisight username that has API priviledges
        password (string):  The password for the above username
        subscriptionKey (string): The subscription key for the above username from the 75F API website
        ids (string): A line separated list of ids to retrieve historical data for (see README.md)
        range (string): The date range to pull historical data for

    Returns:
        results (json):

    """

    authorizationText = SeventyFiveF_Auth.getAuthorization(username, password, subscriptionKey)

    try:
        url = "https://api.75f.io/haystack/hisReadMany"

        hdr ={
            'Authorization': authorizationText,
            'Accept': 'application/json',
            'Content-Type': 'text/zinc',
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': subscriptionKey,
        }

        # The list sent to the 75F API (ids) must consist of one id on each line without any leading or trailing spaces.
        data = \
f"""ver:\"3.0\" range:\"{range}\"
id
{ids}"""

        response = requests.post(url, data=data, headers=hdr, timeout=30)
        return json.loads(response.text)

    except Exception as e:
        return "{'Exception', e}"