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

    Attributes:
        table (Pandas DataFrame): the dataframe to be transformed.
        find_info (Python Class): the DataFrameInfo class initialised with this instance of the dataframe for providing information relating to the dataframe.
    """
    def __init__(self, table):
        self.table = table
        self.find_info = DataFrameInfo(self.table)
       
    def drop_columns(self, columns):
        self.table.drop(columns, axis=1, inplace=True, errors='ignore')
        return self.table
        
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
        for column, skew in skew_table.items():
            if skew > 1:
                boxcox_sample = self.table[column]
                boxcox_sample = boxcox_sample + 1e-10
                boxcox_transform, _ = stats.boxcox(boxcox_sample, lmbda=None)
                boxcox_data = pd.Series(boxcox_transform, name=f'{column}_boxcox')
                self.table = pd.concat([self.table, boxcox_data], axis=1)
                plot = sns.histplot(boxcox_data, label=f'Skewness: {boxcox_data.skew():.2f}')
        plot.legend()  
        return self.table
        
    def yeojohnson_transform(self, skew_table):
        for column, skew in skew_table.items():
            if skew > 1:  
                yeojohnson_data = self.table[column]
                yeojohnson_data = stats.yeojohnson(yeojohnson_data)
                yeojohnson_data= pd.Series(yeojohnson_data[0])
                self.table[column] = yeojohnson_data
                plot=sns.histplot(yeojohnson_data,label="Skewness: %.2f"%(yeojohnson_data.skew()))
                plot.legend()
        return self.table
        
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
                        self.table.iloc[index, self.table.columns.get_loc(column_name)] = median
        return self.table