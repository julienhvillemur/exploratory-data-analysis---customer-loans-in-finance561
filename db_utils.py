#%%

# Import necessary modules
from datetime import datetime


from sqlalchemy import create_engine


import pandas as pd


import yaml


# Load the credentials yaml file
def retrieve():
    with open('credentials.yaml', 'r') as file:
        credentials = yaml.safe_load(file)
    
    return credentials

# Initialise the data extraction class
class RDSDatabaseConnector:

    def __init__(self, credentials):
        self.credentials = credentials

    # Initialise the connection details
    def initialise_details(self):
        database_type = 'postgresql'
        dbapi = 'psycopg2'
        host = self.credentials['RDS_HOST']
        password = self.credentials['RDS_PASSWORD']
        user = self.credentials['RDS_USER']
        database = self.credentials['RDS_DATABASE']
        port = self.credentials['RDS_PORT']

        # Initilise and return SQLAlchemy engine
        engine = create_engine(f"{database_type}+{dbapi}://{user}:{password}@{host}:{port}/{database}")
        return engine
       
    # Connect to RDS Database and return table
    def database_connection(self):
        engine = self.initialise_details()
        with engine.execution_options(isolation_level='AUTOCOMMIT').connect() as conn:
            loan_payments = pd.read_sql_table('loan_payments', engine)
            return loan_payments

    # Save table as CSV file to local machine
    def save_file(self):
        loan_payments = self.database_connection()
        loan_payments.to_csv('../../file_saves/loan_payments.csv', index=False)


# Load CSV file as dataframe from local machine
def open_table():
    with open('../../file_saves/loan_payments.csv', 'r') as file:
        saved_loan_payments_table = pd.read_csv(file)
    return saved_loan_payments_table


class DataTransform:
    """
    Initialise class for converting columns to correct format.
    """
    def __init__(self, loan_payments):
        """
        Initialise class parameters.
        """
        self.loan_payments = loan_payments

    def remove_term_column_strings(self):
        self.loan_payments['term'] = self.loan_payments['term'].str.split(' ').str[0]
        return self.loan_payments
        
    def convert_to_date(self, loan_payments, column_name):
        """
        Convert date columns from MMM-YY to datetime format.
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




#TEST. DELETE ONCE COMPLETE.
credentials = retrieve()

call = RDSDatabaseConnector(credentials)

table = open_table()

table.dtypes

transform_call = DataTransform(table)

transform_call.remove_term_column_strings()

transform_call.iterate_through_columns()


# %%
