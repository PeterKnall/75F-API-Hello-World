import pandas as pd

class DataFrameTools:
    def __init__(self):
        pass

    def restructure_dataframe_on_index(self, df, index, target, value):
        """
        Read in a Pandas Dataframe and return a new Dataframe that:
         1) Add rows to the new dataframe based on unique entries in "index" of the existing dataframe
         2) Adds columns to the new dataframe that have a "domainName" field in target
         3) Adds the "value" column of the cell selected in #2 to the new dataframe
        :param df:
        :return:
        """
        unique_index = set(df[index])                                       # Get a set of unique indices
        unique_target_names = set(df[target])                               # Get a set of unique target columns

        first_column = unique_target_names.pop()
        df_a = df[df[target]==first_column]

        for item in unique_target_names:
            df_b =  df[df[target] == item]
            df_a[item] = df_b[value]

        print(unique_index)
        print(unique_target_names)
        return df_a
