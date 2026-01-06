import SeventyFiveF.ReadByFilter as ReadByFilter
import pandas as pd
import SeventyFiveF.Auth as Auth

class SeventyFiveF_API:
    """
    Commonly used functions for the 75F API.
    """
    def __init__(self, username, password, subscription_key):
        """
        Frequently used functions for the 75F API.
        :param username: Facilisight Username
        :param password: Facilisight Password
        :param subscription_key: API Key from 75F API Management portal
        """
        self.username = username
        self.password = password
        self.subscription_key = subscription_key
        self.authorization_string = Auth.get_authorization(self.username, self.password, self.subscription_key)

    def get_df_by_filter(self, query_string):
        """
        Retrieves data from the 75F API and returns the data in a Pandas DataFrame.
        :param query_string: A Haystack Query to select the desired data.
        :return: A Pandas Dataframe with the data returned from the API.
        :exception: Raises exception for caller to handle
        """
        try:
            reader = ReadByFilter.ReadByFilter(self.username, self.password, self.subscription_key, query_string)
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
            raise Exception(f"Exception in get_all_site_ids_df(\'building and equip\': {e}")

    def get_all_equips_from_site_df(self, site_ref):
        '''
        Given a site id, return a Pandas DataFrame of equipment references.
        :param site_ref: site reference id (e.g., 12346578-1234-1234-1234-1234567890)
        :return: Pandas DataFrame with all equipment ids from the given site
        '''
        try:
            return self.get_df_by_filter(f"equip and siteRef==@{site_ref}")
        except Exception as e:
            raise Exception(f"Error during get_all_equips_from_site")

    def get_all_rooms_from_site_df(self, site_ref):
        '''
        Given a site id return a Pandas DataFrame of room references.
        :param site_ref:  site reference id (e.g., 12346578-1234-1234-1234-1234567890)
        :return: Pandas DataFrame with all room reference ids from the given site
        '''
        try:
            return self.get_df_by_filter(f"room and siteRef==@{site_ref}")
        except Exception as e:
            raise Exception(f"Error during get_all_equips_from_site")

    def get_hist_by_ids(self, ids, range):
        '''
        Retrieve historian data using a list of point ids.
        :param ids: A list of IDs to retrieve historian data for
        :param range: The range of dates to retrieve historian data for
        :return: Pandas DataFrame with the historian data
        '''
        pass

    def get_ids_by_query(self, query_string):
        '''
        Retrieve historian data using a query.
        :param query_string: Query string to identify historian points
        :param range: The range of dates to retrieve historian data for
        :return: Pandas DataFrame with the historian data
        '''
        pass

    def get_room_name_from_room_ref(self, id):
        pass
