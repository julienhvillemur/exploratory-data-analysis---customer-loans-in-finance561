# Import necessary modules.
from scipy import stats


import matplotlib


import matplotlib.pyplot as plt


import pandas as pd


seaborn as sns


class DataFrameTransform:
    """
    Initialise the class for performing EDA transformations.
    """
    def __init__(self, table, null_percentages_table, null_columns, low_skew_columns, categorical_columns, high_skew_columns, date_columns, skew_table):
        self.table = table
        self.null_percentages_table = null_percentages_table
        self.null_columns = null_columns
        self.low_skew_columns = low_skew_columns
        self.categorical_columns = categorical_columns
        self.high_skew_columns = high_skew_columns
        self.date_columns = date_columns
        self.skew_table = skew_table
       
    def drop_columns(self):
        return self.table.drop(self.null_columns, axis=1, inplace=True)
        
    def impute_with_mean(self):
        """
        Impute null values with the mean of columns with < 10% null values respectively.
        """
        for column_name in self.low_skew_columns:
            mean = find_info.get_column_mean(column_name)
            self.table[column_name].fillna(mean, inplace=True)
        return self.table
    
    def impute_with_mode(self):
        for column_name in self.categorical_columns:
            mode = find_info.get_mode(column_name)
            self.table[column_name].fillna(mode, inplace=True)
        return self.table
    
    def impute_with_median(self):
        for column_name in self.high_skew_columns:
            median = find_info.get_median(column_name)
            self.table[column_name].fillna(median, inplace=True)
        return self.table

    def drop_rows(self):
        self.table.dropna(subset=self.date_columns, inplace=True)
        return self.table
    
    def boxcox_transform_skew(self):
        for column, skew in self.skew_table:
            if skew > 1:
                boxcox_sample = self.table[column]
                boxcox_transform = stats.boxcox(boxcox_sample)
                boxcox_data = pd.Series(boxcox_transform[0])
                plot = sns.histplot(boxcox_data, label='Skewness: %.2f'%(boxcox_data.skew()))
            return plot.legend()
