# Simple script to obtain an authorization code from 75F's API
# Uses the "Peter-AES-Production ReadHisWrite" subscription and API/Facilisight credentials
# Uses the Primary API Key

# Output lines labelled "Requests" show the response using the "Requests" library
# Output lines labelled "urllib" show the response using the "urllib" library

# Example was written for Python 3.2
# Uses Python 3.10.11

import os
import requests
import re
import json
import urllib.request


def getAuthorization(username, password, subscriptionKey):
    """Retrieves the Authorization Key using the username, password, and subscription key.  Prepends 'Bearer ' per 75F docs."""
    authorizationText = ""
    try:
        url = "https://api.75f.io/oauth/token"

        hdr ={
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Cache-Control' : 'no-cache',
        'Ocp-Apim-Subscription-Key' : subscriptionKey
        }

        data = {
            "grant_type" : "client_credentials",
            "client_id" : username,
            "client_secret" : password
        }

        # Using requests
        response = requests.post(url, data=data, headers=hdr, timeout=15)
        matches = re.findall(r'"(.*?)"', response.text)
        if len(matches) >= 2:
            authorizationText = 'Bearer ' + matches[1]
            print(f"Requests: {authorizationText}")
    except Exception as e:
        print(f"Requests: {e}")

    # using urllib.request - retained for troubleshooting purposes
    try:
        data = json.dumps(data)
        req = urllib.request.Request(url, headers=hdr, data = bytes(data.encode("utf-8")))

        req.get_method = lambda: 'POST'
        response = urllib.request.urlopen(req)
        print(f"urllib: {response.getcode()}")  # results in HTTP Error 401: Unauthorized
        print(f"urllib: {response.read()}")
    except Exception as e:
        print(f"urllib: {e}")

    return authorizationText