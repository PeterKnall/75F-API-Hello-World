# Read
# This API provides operations for reading and writing operational data to writable points as well as historizing
# data for any point type.

# Read by filter: ver:"3.0" filter "system and equip and siteRef==@b8a1a5be-3080-40e6-9161-64f39944db9e"
# Read by filter (paged): ver:"3.0" size:25 page:3 filter "system and equip and siteRef==@b8a1a5be-3080-40e6-9161-64f39944db9e"
# Read by filter (arrow operator): ver:"3.0" id,dis,equip,siteRef,system @6d78f1c0-d10a-4482-8058-db328441a669,"System Equip A",M,@b8a1a5be-3080-40e6-9161-64f39944db9e,M @84010772-46ec-4937-9430-71083196f2c4,"System Equip B",M,@b8a1a5be-3080-40e6-9161-64f39944db9e,M
# Read by id: ver:"3.0" id @6d78f1c0-d10a-4482-8058-db328441a669 @84010772-46ec-4937-9430-71083196f2c4

########### Python 3.2 #############
import json
import requests
import SeventyFiveF.Auth as Auth

class Read:
    def __init__(self, username, password, subscription_key):
        self.username = username
        self.password = password
        self.subscription_key = subscription_key
        self.authorization_string = Auth.get_authorization(username, password, subscription_key)
        self.url = "https://api.75f.io/haystack/read"

    def post(self):
        self.hdr = {
            'Authorization': self.authorization_string,
            'Accept': 'application/json',
            'Content-Type': 'text/zinc',
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': self.subscription_key,
        }
        data = self.get_body()
        try:
            response = requests.post(self.url, data=data, headers=self.hdr, timeout=30)
            return json.loads(response.text)
        except Exception as e:
            raise Exception(f"Exception during SeventyFiveF.Read(): {e}")

    def get_body(self):
        pass