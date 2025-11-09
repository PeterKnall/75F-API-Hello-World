# Read
# This API provides operations for reading and writing operational data to writable points as well as historizing
# data for any point type.

# Read by filter: ver:"3.0" filter "system and equip and siteRef==@b8a1a5be-3080-40e6-9161-64f39944db9e"
# Read by filter (paged): ver:"3.0" size:25 page:3 filter "system and equip and siteRef==@b8a1a5be-3080-40e6-9161-64f39944db9e"
# Read by filter (arrow operator): ver:"3.0" id,dis,equip,siteRef,system @6d78f1c0-d10a-4482-8058-db328441a669,"System Equip A",M,@b8a1a5be-3080-40e6-9161-64f39944db9e,M @84010772-46ec-4937-9430-71083196f2c4,"System Equip B",M,@b8a1a5be-3080-40e6-9161-64f39944db9e,M
# Read by id: ver:"3.0" id @6d78f1c0-d10a-4482-8058-db328441a669 @84010772-46ec-4937-9430-71083196f2c4

########### Python 3.2 #############
import urllib.request, json, requests
import SeventyFiveF.Auth as Auth


def by_id(username, password, subscription_key, this_id):

    url = "https://api.75f.io/haystack/read"
    authorization_string = Auth.get_authorization(username, password, subscription_key)

    hdr ={
        'Authorization': authorization_string,
        'Accept': 'application/json',
        'Content-Type': 'text/zinc',
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # Request body
    data = \
f"""ver:\"3.0\"
id
{this_id}"""
    try:
        response = requests.post(url, data=data, headers=hdr, timeout=30)
        return json.loads(response.text)
    except Exception as e:
        raise Exception(f"Exception during SeventyFiveF.Read.by_id(): {e}")