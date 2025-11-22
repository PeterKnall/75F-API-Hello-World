import pandas as pd

class DataFrameTools:

    def __init__(self):
        pass

    def convert_ts_to_datetime_column(self, df, column1, column2):
        """
        Converts a column of 75F date strings to a column of date objects.  Removes the original column.
        :param df: Target Pandas DataFrame
        :param column1: Name of the target column
        :param column2: Name of the destination column
        :return: Data Frame with column of date objects
        :except: On error, raises an exception for the caller to handle
        """
        # Wrangle the date stamp
        try:
            df['date_value1'] = df[column1].str.split(":", n=1).str[1]          # Remove the "n:" portion of the date stamp
            df['date_value2'] = df['date_value1'].str.split(" ", n=1).str[0]    # Remove the city portion of the date stamp (Detroit)
            df[column2] = pd.to_datetime(df['date_value2'], format="ISO8601")   # Convert to datetime object
            df.drop(columns=[column1, "date_value1", "date_value2"], inplace=True)
            return df
        except Exception as e:
            raise Exception(f"Exception while converting date string column to date objects: {e}")

    def convert_val_to_numeric_value(self, df, column1, column2):
        """
        Converts a column of 75F numeric strings to a column of numerics (float).  Removes the original column.
        :param df: Target Pandas DataFrame
        :param column1: Name of the target column
        :param column2: Name of the destination column
        :return: DataFrame with the column of numeric values
        :except: On error, raises an exception for the caller to handle
        """
        float_pattern = r'[+-]?(\d+(\.\d*)?|\.\d+)'
        try:
            df[column2] = pd.to_numeric(df[column1].str.extract(float_pattern)[0])
            df.drop(columns=[column1], inplace=True)
            return df
        except Exception as e:
            raise Exception("Exception while converting string column to numeric: {e}")