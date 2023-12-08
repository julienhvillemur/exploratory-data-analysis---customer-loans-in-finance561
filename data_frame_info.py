# Import necessary modules
from scipy import stats


from scipy.stats import chi2_contingency


import numpy as np


import pandas as pd


import matplotlib


class DataFrameInfo():
    """
    Initialise class for deriving information about a dataframe.
    """
    def __init__(self, dataframe):
        """
        See help(DataFrameInfo) for accurate signature.
        """
        self.dataframe = dataframe

    def find_column_types(self, *columns):
        """
        Provide the data types in specifed columns or every column of the dataframe if not specified.
        Args:
            columns(list): a list of column names to be characterised by data type (optional).
        Returns:
            Pandas data series: the individual data types within the provided dataframe or dataframe columns.
        """
        if columns:
            for column in columns:
                return self.dataframe[column].dtypes
        else:
            return self.dataframe.dtypes
    
    def get_statistics(self):
        """
        Provides statistical information about the table input.
        Returns:
            pandas.DataFrame: a table of statistical information about the table input.
        """
        return self.dataframe.describe()
    
    def get_unique_values(self, *columns):
        """
        Identifies all unique values and associated counts within the categorical columns passed in for analysis.
        Args:
            columns(list): a list of categorical column names to be assessed for frequency of unique values (optional).
        Returns:
            Pandas data series: the unique values and associated frequencies within categorical columns.
        """
        if columns:
            for column in columns:
                return self.dataframe[column].value_counts()
        else:
            categorical_columns = self.dataframe.select_dtypes(include=['object'])
            all_categories = {}
            for column in categorical_columns:
                all_categories[column] = categorical_columns[column].value_counts()
            return all_categories
    
    def get_dataframe_shape(self):
        """
        Provide the shape of the dataframe input.
        Returns:
            tuple: the NumPy array shape of the dataframe input.
        """
        return self.dataframe.shape

    def percentage_null_values(self):
        """
        Provide the percentage of null values in each column of the table input.
        Return:
            pandas.Series: the percentage of null values against each column of the table input.
        """
        all_null_percentages = {}
        for column in self.dataframe:
            all_null_percentages[column] = self.dataframe[column].isnull().sum() * 100 / len(self.dataframe)
        null_percentages_table = pd.DataFrame.from_dict(all_null_percentages, orient='index', columns=['percentage_null_values'])
        null_percentages_table = null_percentages_table.sort_values(by='percentage_null_values', ascending=False)
        return null_percentages_table.round(2)
    
    def get_column_mean(self, column_name):
        """
        Calculate the mean of each specified column in the table input.
        Args:
            column_name(list): a list of column names for mean calculation.
        Provides:
            int: the calculated mean based on the provided columns rounded to 0 significant figures.
        """
        column = self.dataframe[column_name]
        return column.mean(skipna=True).round(0)
    
    def column_skew(self, *column_names):
        """
        Calculate skew scores for columns in the table input.
        Args:
            column_names(list): the list of column names for assessing skew (optional).
        Returns:
            pandas.Series: the skew scores against each specified column of the table input.
        """
        if column_names:
            skew = []
            for column in column_names:
                skew = self.dataframe[column].skew(numeric_only=True)
            return skew
        else:
            return self.dataframe.skew(numeric_only=True)
    
    def get_mode(self, column_names):
        """
        Calculate the mode of each column in the table input.
        Args:
            column_names(list): a list of column names for calculation of mode.
        Returns:
            float: the value of the mode for the specified table column input.
        """
        return self.dataframe[column_names].mode().values[0]
    
    def get_median(self, column_names):
        """
        Calculate the median for the specified columns in the table input.
        Args:
            column_names(list): a list of column names for calculation of meadian.
        Returns:
            float: the value of the median for the specified table column input.
        """
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

    def chi_square_test(self, customer_type, risk_factors):
        """
        Test statistical relationship between loan_status and risk-factor columns via Chi-square.
        Args:
            customer_type(Pandas dataframe): the loan payments table containing rows isolated to different customer types based on the 'loan_status' column.
            risk_factors(list): a list of columns representing potential risk factors for late loan payments.
        Returns:
            Pandas dataframe: a table containing the Chi-square statistic and p-value for set of tested columns.
        """
        statistics = pd.DataFrame(columns=['Risk Factor', 'Chi-square Statistic', 'p-value'])
        for risk_column in risk_factors:
            contingency_table = pd.crosstab(customer_type['loan_status'], customer_type[risk_column])
            chi2, p, dof, expected = chi2_contingency(contingency_table)
            print(f"Statistical comparison between {risk_column} and loan_status provides a Chi-square statistic of {chi2} and a p-value of {p}")
            new_row = [{'Risk Factor': risk_column, 'Chi-square Statistic': chi2, 'p-value': p}]
            statistics.loc[len(statistics.index)] = [risk_column, chi2, p]
        return statistics