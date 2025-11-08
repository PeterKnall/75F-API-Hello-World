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
# The "requests" library replaced the "urllibs" library, which I could not get to work.

import requests
import re

def get_authorization(username, password, subscription_key):
    """
    Retrieves the Authorization Key using the username, password, and subscription key.  Prepends 'Bearer '
    to the Authorization Code per the 75F documentation.
    Args:
        username (string):  The Facilisight username that has API privileges
        password (string):  The password for the above username
        subscription_key (string): The subscription key for the above username from the 75F API website

    Returns:
        Authorization Key (string): The authorization code from the 75F API for use during future requests.
        Returns an empty string ("") if an Authorization Key is not returned.
    """

    url = "https://api.75f.io/oauth/token"

    hdr ={
    'Content-Type' : 'application/x-www-form-urlencoded',
    'Cache-Control' : 'no-cache',
    'Ocp-Apim-Subscription-Key' : subscription_key
    }

    data = {
        "grant_type" : "client_credentials",
        "client_id" : username,
        "client_secret" : password
    }

    try:
        response = requests.post(url, data=data, headers=hdr, timeout=15)
    except Exception as e:
        return ""  # TODO: Handle or raise Exception as appropriate

    matches = re.findall(r'"(.*?)"', response.text)
    if len is None:
        return "" # TODO: Handle or raise Exception as appropriate
    elif len(matches) >= 2:
        authorization_string = 'Bearer ' + matches[1]
        print(authorization_string)
        return authorization_string
    else:
        return "" # TODO: Handle or raise Exception as appropriate