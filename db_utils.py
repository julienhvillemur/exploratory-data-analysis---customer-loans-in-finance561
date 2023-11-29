#%%

# Import necessary modules
from datetime import datetime


from sqlalchemy import create_engine


import pandas as pd

import missingno as msno
#import seaborn as sns


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
        self.loan_payments['term'] = self.loan_payments['term'].astype('float64')
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
        #filled_column = self.dataframe[column_name].fillna(0, inplace=True)
        #print(filled_column)
        #return self.dataframe[column_name].mean().round(0)
        return self.dataframe[column_name].mean(skipna=True).round(0)
    
    def column_skew(self, column_names):
        for column in column_names:
            return self.dataframe[column].skew()
    
    def get_mode(self, column_names):
        return self.dataframe[column_names].mode().values[0]
    
    def get_median(self, column_names):
        return self.dataframe[column_names].median()

class Plotter:
    """
    Initialise the class for visualising data insights.
    """
    def __init__(self, original_table, clean_table):
        self.original_table = original_table
        self.clean_table = clean_table

    def compare_heatmaps(self):
        # Create correlation matrix for loan payments data:
        sns.heatmap(self.original_table.corr(), annot=True, cmap='coolwarm')
        sns.heatmap(self.clean_table.corr(), annot=True, cmap='coolwarm')

#TEST. DELETE ONCE COMPLETE.
#credentials = retrieve()

#call = RDSDatabaseConnector(credentials)

table = open_table()

# Visualise the raw dataframe.
msno.matrix(table)

old_table = table

transform_call = DataTransform(table)

transform_call.remove_term_column_strings()

transform_call.iterate_through_columns()

find_info = DataFrameInfo(table)

null_percentages_table = find_info.percentage_null_values()

# DRAFT


class DataFrameTransform:
    """
    Initialise the class for performing EDA transformations.
    """
    def __init__(self, table, null_percentages_table, null_columns, low_skew_columns, categorical_columns, high_skew_columns, date_columns):
        self.table = table
        self.null_percentages_table = null_percentages_table
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


# Columns with null values:
all_null_columns = ['mths_since_last_record', 'mths_since_last_major_derog', 'next_payment_date', 'mths_since_last_delinq', 'employment_length', 'last_payment_date', 'last_credit_pull_date','term', 'int_rate', 'funded_amount', 'collections_12_mths_ex_med']

 # Columns with >50% null values:
highest_null_proportion_columns = ['mths_since_last_record', 'mths_since_last_major_derog', 'next_payment_date', 'mths_since_last_delinq']

# Categorical columns:
categorical_columns = ['employment_length', 'term'] # Contains null values

# Date columns
date_columns = ['last_payment_date', 'last_credit_pull_date'] # Contains null values

# Columns with <10% null values:
low_null_columns = ['int_rate', 'funded_amount', 'last_payment_date', 'last_credit_pull_date', 'collections_12_mths_ex_med']

# Assessing sknewness of columns.
skewness = find_info.column_skew(low_null_columns)

# Columns with <1 skew:
low_skew_columns = ['int_rate', 'funded_amount']

# Columns with >1 skew:
high_skew_columns = ['collections_12_mths_ex_med']

data_frame_transform_call = DataFrameTransform(table, null_percentages_table, highest_null_proportion_columns, low_skew_columns, categorical_columns, high_skew_columns, date_columns)

# Drop all columns with >50% null values.
data_frame_transform_call.drop_columns()

# Impute all null values in columns with <10% null values.
data_frame_transform_call.impute_with_mean()

#find_info.column_skew()
find_info.find_column_types(low_skew_columns)

# Impute null values in categorical columns with mode.
data_frame_transform_call.impute_with_mode()

# Impute null values in columns with >1 skew with median.
data_frame_transform_call.impute_with_median()

# Drop rows with null values in columns with <1% null values.
new_table = data_frame_transform_call.drop_rows()

new_info = DataFrameInfo(new_table)

new_null = new_info.percentage_null_values()

#plotter_call = Plotter(old_table, new_table)
#plotter_call.compare_heatmaps

# %%
