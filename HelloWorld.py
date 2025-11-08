import SeventyFiveF_hisReadMany
import SeventyFiveF_Read
import os
import pandas as pd

username = os.environ.get("75F API Username")
password = os.environ.get("75F API Password")
subscriptionKey = os.environ.get("75F API Subscription Key")

date_range = "today"

id = "@52bdc021-71d3-4479-903e-0b0986a993ee"
ids = """@52bdc021-71d3-4479-903e-0b0986a993ee @52b2309a-10ec-4578-af76-8c1130c58044"""
itemList = ids.split(" ")
items = '\n'.join(itemList)

result = SeventyFiveF_Read.get_read(username, password, subscriptionKey, id)
#results = SeventyFiveF_hisReadMany.get_hisReadMany(username, password, subscriptionKey, items, date_range)
#df = pd.read_json(results)
#df1.to_csv(df, index=False)
#print (df1)
print(result)
