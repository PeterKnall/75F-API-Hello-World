import os
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
        :exception: Echo error to console and return an empty dataframe
        """
        try:
            reader = ReadByFilter.ReadByFilter(self.username, self.password, self.subscriptionKey, query_string)
            result = reader.post()
            return pd.DataFrame(result["rows"])
        except Exception as e:
            print(f"Error during get_df_by_filter(\'{query_string}\': {e}")
            return pd.DataFrame()

    def get_all_site_ids_df(self):
        """
        Retrieves all the sites the user has access to.
        :return: Pandas DataFrame
        """
        try:
            return self.get_df_by_filter("building and equip")
        except Exception as e:
            print(f"Error during get_df_by_filter(\'building and equip\': {e}")
            return pd.DataFrame()

    def remove_building_equip_text(self, display_name_string):
        """
        Splits the string on "-" and returns the first match.  Effective in removing the "-buildingEquip" text
        from a string.
        :param display_name_string: Display Name ('dis')
        :return: Display Name with the "-buildingEquip" removed
        """
        if "-" in display_name_string:
            return display_name_string.split("-")[0]
        else:
            return display_name_string