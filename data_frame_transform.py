# Import necessary modules.
from data_frame_info import DataFrameInfo


from scipy import stats


import matplotlib


import matplotlib.pyplot as plt


import pandas as pd


import numpy as np


import seaborn as sns


class DataFrameTransform:
    """
    Initialise the class for performing EDA transformations.
    """
    def __init__(self, table):
        self.table = table
        self.find_info = DataFrameInfo(self.table)
       
    def drop_columns(self, columns):
        return self.table.drop(columns, axis=1, inplace=True)
        
    def impute_with_mean(self, columns):
        """
        Impute null values with the mean of columns with < 10% null values respectively.
        """
        for column_name in columns:
            mean = self.find_info.get_column_mean(column_name)
            self.table[column_name].fillna(mean, inplace=True)
        return self.table
    
    def impute_with_mode(self, columns):
        for column_name in columns:
            mode = self.find_info.get_mode(column_name)
            self.table[column_name].fillna(mode, inplace=True)
        return self.table
    
    def impute_with_median(self, columns):
        for column_name in columns:
            median = self.find_info.get_median(column_name)
            self.table[column_name].fillna(median, inplace=True)
        return self.table

    def drop_rows(self, columns):
        self.table.dropna(subset=columns, inplace=True)
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
        
    def impute_outliers(self):
        """
        Impute outliers in high skew columns with the median.
        """
        skew_table = self.find_info.column_skew()
        for column_name, data in self.table.select_dtypes(include='number').items():
            if skew_table.loc[column_name] > 1:
                for index, z_score in enumerate(stats.zscore(self.table[column_name])):
                    if z_score > 3:
                        median = self.find_info.get_median(column_name)
                        self.table.iloc[self.table.columns.get_loc(column_name), index] = median
        return self.table