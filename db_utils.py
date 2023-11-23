#%%

# Import necessary modules
import yaml


from sqlalchemy import create_engine


import pandas as pd


# Load the credentials yaml file
def retrieve():
    with open('credentials.yaml', 'r') as file:
        credentials = yaml.safe_load(file)
    
    return credentials

# Initialise the data extraction class
class RDSDatabaseConnector():

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

        # Make engine a global variable and initilise SQLAlchemy engine
        global engine
        engine = create_engine(f"{database_type}+{dbapi}://{user}:{password}@{host}:{port}/{database}")
       
    # Connect to RDS Database and return table
    def database_connection(self):
        with engine.execution_options(isolation_level='AUTOCOMMIT').connect() as conn:
            global loan_payments
            loan_payments = pd.read_sql_table('loan_payments', engine)

    # Save table as CSV file to local machine
    def save_file(self):
        loan_payments.to_csv('../../file_saves/loan_payments.csv', index=False)


# Load CSV file as dataframe from local machine
def open_table():
    with open('../../file_saves/loan_payments.csv', 'r') as file:
        saved_table = pd.read_csv(file)
    return saved_table


#TEST. DELETE ONCE COMPLETE.
credentials = retrieve()

call = RDSDatabaseConnector(credentials)

open_table().shape

# %%
