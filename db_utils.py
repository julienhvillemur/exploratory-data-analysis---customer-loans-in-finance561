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


class DataFrameInfo():
    """
    Initialise class for deriving information about a dataframe.
    """
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def find_column_types(self):
        """
        Return the data types in every column of the dataframe.
        """
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
        filled_column = self.dataframe[column_name].fillna(0, inplace=True)
        return self.dataframe[column_name].mean().round(0)
    

class Plotter:
    """
    Initialise the class for visualising data insights.
    """
    def __init__(self, table):
        self.table = table


#TEST. DELETE ONCE COMPLETE.
credentials = retrieve()

call = RDSDatabaseConnector(credentials)

table = open_table()

transform_call = DataTransform(table)

transform_call.remove_term_column_strings()

transform_call.iterate_through_columns()

find_info = DataFrameInfo(table)

#find_info.get_column_mean()

null_percentages_table = find_info.percentage_null_values()
# DRAFT


class DataFrameTransform:
    """
    Initialise the class for performing EDA transformations.
    """
    def __init__(self, table, null_percentages_table, null_columns, low_null_columns):
        self.table = table
        self.null_percentages_table = null_percentages_table
        self.null_columns = null_columns
        self.low_null_columns = low_null_columns
       
    def drop_columns(self):
        reduced_table = self.table.drop(self.null_columns, axis=1)
        return reduced_table
        # DRAFT automatic column drop.
        #reduced_table = [column.drop(columns=index) for column in self.table if self.null_percentages_table['percentage_null_values'] > 50]
        #return reduced_table
        
    def impute_values(self):
        """
        Impute null values with the mean of columns with < 10% null values respectively.
        """
        for column_name in self.low_null_columns:
            print(column_name)
            mean = find_info.get_column_mean(column_name)
            print(mean)
            self.table[column_name].fillna(mean, inplace=True)
        return self.table


 # Columns with >50% null values
highest_null_proportion_columns = ['mths_since_last_record', 'mths_since_last_major_derog', 'next_payment_date', 'mths_since_last_delinq']

# Columns with <10% null values
low_null_columns = ['int_rate', 'funded_amount', 'last_payment_date', 'collections_12_mths_ex_med', 'last_credit_pull_date']

# Columns unable to be imputed under the current method
unchanged_columns = ['term', 'employment_length', ]

data_frame_transform_call = DataFrameTransform(table, null_percentages_table, highest_null_proportion_columns, low_null_columns)

# Drop all columns with > 50% null values
data_frame_transform_call.drop_columns()

# Impute all null values in columns with <10% null values
display(table)
data_frame_transform_call.impute_values()

# %%
