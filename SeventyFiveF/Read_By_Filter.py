# Read
# This API provides operations for reading and writing operational data to writable points as well as historizing
# data for any point type.

# Read by filter: ver:"3.0" filter "system and equip and siteRef==@b8a1a5be-3080-40e6-9161-64f39944db9e"

import SeventyFiveF.Read as SeventyFiveF

class Read_By_Filter(SeventyFiveF.Read):
    def __init__(self, username, password, subscription_key, read_argument):
        super().__init__(username, password, subscription_key)
        self.read_argument = read_argument

    def get_body(self):
        data = f"ver:\"3.0\"\nfilter\n\"{self.read_argument}\""
        return data