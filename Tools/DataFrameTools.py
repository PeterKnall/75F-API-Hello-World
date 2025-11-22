import pandas as pd

class DataFrameTools:

    def __init__(self):
        pass

    def convert_ts_to_datetime_column(self, df, column1, column2):
        '''
        Converts a column of 75F date strings to a column of date objects
        :param df: Target Pandas DataFrame
        :param column1: Name of the target column
        :param column2: Name of the destination column
        :return: Data Frame with column of date objects
        '''
        # Wrangle the date stamp
        df['date_value1'] = df[column1].str.split(":", n=1).str[
            1]  # Remove the "n:" portion of the date stamp
        df['date_value2'] = df['date_value1'].str.split(" ", n=1).str[
            0]  # Remove the city portion of the date stamp (Detroit)
        df[column2] = pd.to_datetime(df['date_value2'], format="ISO8601")  # Convert to datetime object
        df.drop(columns=["date_value1", "date_value2"], inplace=True)
        return df