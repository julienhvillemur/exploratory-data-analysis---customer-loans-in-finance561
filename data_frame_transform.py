# Import necessary modules.
from data_frame_info import DataFrameInfo


from scipy import stats


import matplotlib


import matplotlib.pyplot as plt


import pandas as pd


import seaborn as sns


class StatsChanges:
    """
    Initialise the class for performing EDA transformations.
    """
    def __init__(self, table, null_columns, low_skew_columns, categorical_columns, high_skew_columns, date_columns):
        self.table = table
        self.find_info = DataFrameInfo(self.table)
        self.null_columns = null_columns
        self.low_skew_columns = low_skew_columns
        self.categorical_columns = categorical_columns
        self.high_skew_columns = high_skew_columns
        self.date_columns = date_columns
       
    def drop_columns(self):
        return self.table.drop(self.null_columns, axis=1, inplace=True)
        
    def impute_with_mean(self):
        """
        Impute null values with the mean of columns with < 10% null values respectively.
        """
        for column_name in self.low_skew_columns:
            mean = self.find_info.get_column_mean(column_name)
            self.table[column_name].fillna(mean, inplace=True)
        return self.table
    
    def impute_with_mode(self):
        for column_name in self.categorical_columns:
            mode = self.find_info.get_mode(column_name)
            self.table[column_name].fillna(mode, inplace=True)
        return self.table
    
    def impute_with_median(self):
        for column_name in self.high_skew_columns:
            median = self.find_info.get_median(column_name)
            self.table[column_name].fillna(median, inplace=True)
        return self.table

    def drop_rows(self):
        self.table.dropna(subset=self.date_columns, inplace=True)
        return self.table
    
    def boxcox_transform(self, skew_table):
        for column, skew in skew_table:
            if skew > 1:
                boxcox_sample = self.table[column]
                boxcox_transform = stats.boxcox(boxcox_sample)
                boxcox_data = pd.Series(boxcox_transform[0])
                plot = sns.histplot(boxcox_data, label='Skewness: %.2f'%(boxcox_data.skew()))
            return plot.legend()
        
    def yeojohnson_transform(self, skew_table):
        for column, skew in skew_table.items():
            if skew > 1:      
                yeojohnson_sample = self.table[column]
                yeojohnson_transform = stats.yeojohnson(yeojohnson_sample)
                yeojohnson_data= pd.Series(yeojohnson_transform[0])
                plot=sns.histplot(yeojohnson_data,label="Skewness: %.2f"%(yeojohnson_data.skew()) )
            return plot.legend()