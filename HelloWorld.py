import SeventyFiveF_hisReadMany
import os

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

date_range = "today"

ids = """@52bdc021-71d3-4479-903e-0b0986a993ee @52b2309a-10ec-4578-af76-8c1130c58044"""
itemList = ids.split(" ")
items = '\n'.join(itemList)

print(SeventyFiveF_hisReadMany.get_hisReadMany(username, password, subscriptionKey, items, date_range))
