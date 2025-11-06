# Simple script to obtain an authorization code from 75F's API
#
# A special thanks for the following supporters:
#
# Permanently deleted user (5 Nov 2025):
# Link-1 : https://support.75f.io/hc/en-us/articles/5460179115923-HisReadMany-API?input_string=auth+and+hisreadmany+api+help
# Link-2 : https://support.75f.io/hc/en-us/articles/5460365803027-75F-API-s-Error-Returns?input_string=auth+and+hisreadmany+api+help
#
# This example was pulled from the 75F API website and written for Python 3.2.
# This example was executed in Python 3.10.11

import requests
import re

def getAuthorization(username, password, subscriptionKey):
    """
    Retrieves the Authorization Key using the username, password, and subscription key.  Prepends 'Bearer '
    to the Authorization Code per the 75F documentation.
    Args:
        username (string):  The Facilisight username that has API priviledges
        password (string):  The password for the above username
        subscriptionKey (string): The subscription key for the above username from the 75F API website

    Returns:
        Authorization Key (string): The authorization code from the 75F API for use during future requests.
        Returns an empty string ("") if an Authorization Key is not returened.
    """

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

    response = ""
    try:
        response = requests.post(url, data=data, headers=hdr, timeout=15)
    except Exception as e:
        return ""  # TODO: Handle or raise Exception as appropriate

    matches = re.findall(r'"(.*?)"', response.text)
    if len == None:
        return "" # TODO: Handle or raise Exception as appropriate
    elif len(matches) >= 2:
        authorizationText = 'Bearer ' + matches[1]
        return authorizationText
    else:
        return "" # TODO: Handle or raise Exception as appropriate