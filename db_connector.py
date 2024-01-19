# Import necessary modules
from sqlalchemy import create_engine


import pandas as pd


import yaml
 

# Restrict usage of the RDSDataBase class and the retrieve() function to this file.
class RDSDatabaseConnector:
    """
    Initialise class for data extraction from an RDS database.

    Attributes:
        credentials (.yaml file): a file containing the credential details necessary from access to the RDS database.
    """

    def __init__(self, credentials):
        """
        See help(RDSDatabaseConnector) for accurate signature.
        """
        self.credentials = credentials

    def initialise_details(self):
        """
        Initialise the connection details and pass into an SQLAlchemy engine.
        Returns:
            Engine: SQLAlchemy engine for use in the database_connection method.
        """
        database_type = 'postgresql'
        dbapi = 'psycopg2'
        host = self.credentials['RDS_HOST']
        password = self.credentials['RDS_PASSWORD']
        user = self.credentials['RDS_USER']
        database = self.credentials['RDS_DATABASE']
        port = self.credentials['RDS_PORT']

        engine = create_engine(f"{database_type}+{dbapi}://{user}:{password}@{host}:{port}/{database}")
        return engine
    
    def database_connection(self):
        """
        Connect to RDS Database to retrieve the loan_payments table.
        Returns:
            pandas.Dataframe: a table containing multiple loans and associated data.
        """
        engine = self.initialise_details()
        with engine.execution_options(isolation_level='AUTOCOMMIT').connect() as conn:
            loan_payments = pd.read_sql_table('loan_payments', engine)
            return loan_payments

    def save_file(self):
        """
        Save the loan_payments dataframe as a CSV file to the local directory.
        Enables efficient table access in the EDA project.
        """
        loan_payments = self.database_connection()
        loan_payments.to_csv('loan_payments.csv', index=False)


def retrieve():
    """
    Load the credentials yaml file from the local directory.
    Returns:
        yaml file: a file containing the credentials
    """
    with open('credentials.yaml', 'r') as file:
        credentials = yaml.safe_load(file)
    
    return credentials

# Open the locally saved credentials yaml file for access to the RDS database.
credentials = retrieve()

# Call the RDSDatabaseConnector Class with the credentials yaml file.
connect_to_database = RDSDatabaseConnector(credentials)

# Call the save_file method to retrieve and save loan_payments.csv to the local directory.
connect_to_database.save_file()


def open_table():
    """
    Load loan_payments CSV file as dataframe from local directory.
    Returns:
        pandas.DataFrame: a table of loan data to be used in the EDA project.
    """
    with open('loan_payments.csv', 'r') as file:
        saved_loan_payments_table = pd.read_csv(file)
    return saved_loan_payments_table


def open_null_removed_table():
    """
    Load null-removed loan_payments CSV file as dataframe from local directory.
    Returns:
        pandas.DataFrame: a table of loan data without null values.
    """
    with open('null_removed_table.csv', 'r') as file:
        no_null_loan_payments_table = pd.read_csv(file)
    return no_null_loan_payments_table


def open_transformed_table():
    """
    Load transformed loan_payments CSV file as dataframe from local directory.
    Returns:
        pandas.DataFrame: a table of loan data transformed by imputation, data removal and skew correction.
    """
    with open('transformed_table.csv', 'r') as file:
        transformed_loan_payments_table = pd.read_csv(file)
    return transformed_loan_payments_table


def open_latest_table():
    """
    Load latest transformation of the loan_payments file in the local directory.
    Returns:
        pandas.DataFrame: a table of loan data transformed by imputation, data removal, skew correction and outlier imputation.
    """
    with open('refined_table.csv', 'r') as file:
        latest_loan_payments_table = pd.read_csv(file)
    return latest_loan_payments_table
    