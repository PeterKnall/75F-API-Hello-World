import SeventyFiveF.ReadByFilter as ReadByFilter
import pandas as pd

class SeventyFiveF_API:
    """
    Commonly used functions for the 75F API.
    """
    def __init__(self, username, password, subscriptionKey):
        """
        Frequently used functions for the 75F API.
        :param username: Facilisight Username
        :param password: Facilisight Password
        :param subscriptionKey: API Key from 75F API Management portal
        """
        self.username = username
        self.password = password
        self.subscriptionKey = subscriptionKey

    def get_df_by_filter(self, query_string):
        """
        Retrieves data from the 75F API and returns the data in a Pandas DataFrame.
        :param query_string: A Haystack Query to select the desired data.
        :return: A Pandas Dataframe with the data returned from the API.
        :exception: Raises exception for caller to handle
        """
        try:
            reader = ReadByFilter.ReadByFilter(self.username, self.password, self.subscriptionKey, query_string)
            result = reader.post()
            return pd.DataFrame(result["rows"])
        except Exception as e:
            raise Exception(f"Error during get_df_by_filter(\'{query_string}\': {e}")

    def get_all_site_ids_df(self):
        """
        Retrieves all the sites the user has access to.
        :return: Pandas DataFrame
        :exception: Raises exception for caller to handle
        """
        try:
            return self.get_df_by_filter("building and equip")
        except Exception as e:
            raise Exception(f"Error during get_all_site_ids_df(\'building and equip\': {e}")