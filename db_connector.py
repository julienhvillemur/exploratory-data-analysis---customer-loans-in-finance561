# Import necessary modules
from sqlalchemy import create_engine


import pandas as pd


import yaml
 

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


# Load the credentials yaml file
def retrieve():
    with open('credentials.yaml', 'r') as file:
        credentials = yaml.safe_load(file)
    
    return credentials


# Load CSV file as dataframe from local machine
def open_table():
    with open('../../file_saves/loan_payments.csv', 'r') as file:
        saved_loan_payments_table = pd.read_csv(file)
    return saved_loan_payments_table