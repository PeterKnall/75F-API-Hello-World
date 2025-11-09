# Read
# This API provides operations for reading and writing operational data to writable points as well as historizing
# data for any point type.

# Read by id: ver:"3.0" id @6d78f1c0-d10a-4482-8058-db328441a669 @84010772-46ec-4937-9430-71083196f2c4

import SeventyFiveF.Read as SeventyFiveF

class Read_By_Id(SeventyFiveF.Read):
    def __init__(self, username, password, subscription_key, read_argument):
        super().__init__(username, password, subscription_key)
        self.read_argument = read_argument

    def get_body(self):
        return f"ver:\"3.0\"\nid\n{self.read_argument}"