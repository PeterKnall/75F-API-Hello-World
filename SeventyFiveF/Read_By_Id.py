# Read
# This API provides operations for reading and writing operational data to writable points as well as historizing
# data for any point type.

# Read by filter: ver:"3.0" filter "system and equip and siteRef==@b8a1a5be-3080-40e6-9161-64f39944db9e"
# Read by filter (paged): ver:"3.0" size:25 page:3 filter "system and equip and siteRef==@b8a1a5be-3080-40e6-9161-64f39944db9e"
# Read by filter (arrow operator): ver:"3.0" id,dis,equip,siteRef,system @6d78f1c0-d10a-4482-8058-db328441a669,"System Equip A",M,@b8a1a5be-3080-40e6-9161-64f39944db9e,M @84010772-46ec-4937-9430-71083196f2c4,"System Equip B",M,@b8a1a5be-3080-40e6-9161-64f39944db9e,M
# Read by id: ver:"3.0" id @6d78f1c0-d10a-4482-8058-db328441a669 @84010772-46ec-4937-9430-71083196f2c4

import SeventyFiveF.Read as SeventyFiveF

class Read_By_Id(SeventyFiveF.Read):
    def __init__(self, username, password, subscription_key, read_argument):
        super().__init__(username, password, subscription_key)
        self.read_argument = read_argument

    def get_body(self):
        return f"ver:\"3.0\"\nid\n{self.read_argument}"