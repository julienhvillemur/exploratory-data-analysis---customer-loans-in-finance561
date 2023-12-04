# Import necessary modules
from scipy import stats


import numpy as np


import pandas as pd


import matplotlib


class DataFrameInfo():
    """
    Initialise class for deriving information about a dataframe.
    """
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def find_column_types(self, *columns):
        """
        Return the data types in specifed columns or every column of the dataframe if not specified.
        """
        if columns:
            for column in columns:
                return self.dataframe[column].dtypes
        else:
            return self.dataframe.dtypes
    
    def get_statistics(self):
        """
        Return statistical information about the dataframe.
        """
        return self.dataframe.describe()
    
    def get_unique_values(self):
        """
        Return the unique values within each categorical column.
        """
        categorical_columns = self.dataframe.select_dtypes(include=['object'])
        all_categories = {}
        for column in categorical_columns:
            all_categories[column] = categorical_columns[column].value_counts()
        return all_categories
    
    def get_dataframe_shape(self):
        """
        Return the shape of the dataframe.
        """
        return self.dataframe.shape

    def percentage_null_values(self):
        """
        Return the percentage of null values in each column of the dataframe.
        """
        all_null_percentages = {}
        for column in self.dataframe:
            all_null_percentages[column] = self.dataframe[column].isnull().sum() * 100 / len(self.dataframe)
        null_percentages_table = pd.DataFrame.from_dict(all_null_percentages, orient='index', columns=['percentage_null_values'])
        null_percentages_table = null_percentages_table.sort_values(by='percentage_null_values', ascending=False)
        return null_percentages_table.round(2)
    
    def get_column_mean(self, column_name):
        return self.dataframe[column_name].mean(skipna=True).round(0)
    
    def column_skew(self, *column_names):
        if column_names:
            all_skew = []
            for column in column_names:
                skew = {column:self.dataframe[column].skew(numeric_only=True)}
                all_skew.append(skew)
            return all_skew
        else:
            return self.dataframe.skew(numeric_only=True)
    
    def get_mode(self, column_names):
        return self.dataframe[column_names].mode().values[0]
    
    def get_median(self, column_names):
        return self.dataframe[column_names].median()
    
    def get_histogram(self):
        """
        Generate histogram of provided dataframe.
        Returns:
            NumPy array: histogram of the provided dataframe.
        """
        return self.dataframe.hist(figsize=(15,20))

    def get_zscores(self):
        """
        Provide the z-scores for imputted dataframes.
        Returns:
            Array: the z-scores of all numeric values in the inputted dataframe.
        """
        numeric_columns = self.dataframe.select_dtypes(include=np.number)
        return stats.zscore(numeric_columns)

    def recovered_loans(self):
        """
        Calculate the percentage of total loans and investor loan funds repaid.
        Calculate the percentage of total loans repaid in 6 months.
        Returns(dict): a dictionary of three variables
            percentage_investments_recovered(numpy.float64): the percentage of the total loans amount repaid by customers.
            overall_percentage_recovered(numpy.float64): the percentage of the investor-funded portion of loans repaid by customers.
            percentage_recovered_after_6_months(numpy.float64): the percentage of the total amount paid after 6 months of installments from all customers.
            """
        total_loans = self.dataframe['funded_amount'].sum()
        total_amount_recovered = total_loans - self.dataframe['out_prncp'].sum()
        total_amount_invested = self.dataframe['funded_amount_inv'].sum()
        total_investments_recovered = total_amount_invested - self.dataframe['out_prncp_inv'].sum()
        percentage_investments_recovered = (total_investments_recovered / total_amount_invested * 100).round(2)
        overall_percentage_recovered = (total_amount_recovered / total_loans * 100).round(2)
        total_amount_paid_after_6_months = self.dataframe['instalment'].sum() * 6
        percentage_recovered_after_6_months = (total_amount_paid_after_6_months / total_loans * 100).round(2)
        print(f'The proportion of loan investments recovered is {percentage_investments_recovered}%.')
        print(f'The proportion of whole loans recovered is {overall_percentage_recovered}%.')
        print(f'6 months of customer instalments will result in {percentage_recovered_after_6_months}% loan recovery.')
        return {'Loans Recovered':overall_percentage_recovered, 'Investments Recovered':percentage_investments_recovered, 'Loans Recovered\n After 6 months': percentage_recovered_after_6_months}
