# Import the necessary modules.
from datetime import datetime


import pandas as pd


class DataTransform:
    """
    Initialise class for converting columns to correct the format.

    Attributes:
        loan_payments (pandas.DataFrame): the loan payments table to be used for EDA.
    """
    def __init__(self, loan_payments):
        """
        See help(DataTransform) for accurate signature.
        """
        self.loan_payments = loan_payments

    def remove_term_column_strings(self):
        """
        Removes string from the term column in the loan payments dataframe.
        Returns:
            Pandas dataframe: the loan payments table with the 'term' column in float64 format.
        """
        self.loan_payments['term'] = self.loan_payments['term'].str.split(' ').str[0]
        self.loan_payments['term'] = self.loan_payments['term'].astype('float64')
        return self.loan_payments
        
    def convert_to_date(self, loan_payments, column_name):
        """
        Convert date columns from MMM-YY to datetime format.
        Returns:
            Pandas dataframe: a table with all inputted date columns in the MM-YYYY format.
        """
        loan_payments[column_name] = pd.to_datetime(loan_payments[column_name], format='%b-%Y').dt.to_period('M')
        return loan_payments

    def iterate_through_columns(self):
        """
        Provide every column containing dates for conversion in the convert_to_date method.
        """
        column_names = ['last_payment_date', 'next_payment_date', 'last_credit_pull_date', 'issue_date', 'earliest_credit_line']

        for names in column_names:
            self.convert_to_date(self.loan_payments, names)
        
        return self.loan_payments