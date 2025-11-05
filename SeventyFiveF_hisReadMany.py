# Simple script to retrieve a set of trends from 75F Haystack
# Uses the "Peter-AES-Production ReadHisWrite" subscription and API/Facilisight credentials
# Uses the Primary API Key

# Output lines labelled "Requests" show the response using the "Requests" library
# Output lines labelled "urllib" show the response using the "urllib" library

# Link-1 : https://support.75f.io/hc/en-us/articles/5460179115923-HisReadMany-API?input_string=auth+and+hisreadmany+api+help
# Link-2 : https://support.75f.io/hc/en-us/articles/5460365803027-75F-API-s-Error-Returns?input_string=auth+and+hisreadmany+api+help

# Example was written for Python 3.2
# Uses Python 3.10.11

import requests
import json
import urllib.request
import SeventyFiveF_Auth

def getHisReadMany(username, password, subscriptionKey, ids, range):
    """Retrieves historical data"""

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

        data = f"ver:\"3.0\" range:\"{range}\" id:\"{ids}\""
        print(f"Data: {data}")

        # Using requests
        response = requests.post(url, data=data, headers=hdr, timeout=30)
        print(f"Requests:<{response.text}>")  # results in error: Zinc could not be processed. Offending token located at line: 2, position 0

    except Exception as e:
        print(f"Requests: {e}")

    # using urllib.request - retained for troubleshooting purposes
    try:
        # using urllib.request
        data = json.dumps(data)
        req = urllib.request.Request(url, headers=hdr, data = bytes(data.encode("utf-8")))

        req.get_method = lambda: 'POST'
        response = urllib.request.urlopen(req)
        print(response.getcode())  # results in HTTP Error 401: Unauthorized
        print(response.read())
    except Exception as e:
        print(f"urllib: {e}")

    return "MPL Complete."