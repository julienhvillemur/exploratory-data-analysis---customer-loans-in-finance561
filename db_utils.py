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
       
    # Connect to RDS Database
    def database_connection(self):
        with engine.execution_options(isolation_level='AUTOCOMMIT').connect() as conn:
            loan_payments = pd.read_sql_table('loan_payments', engine)
            display(loan_payments.head(10))


#TEST. DELETE ONCE COMPLETE.
credentials = retrieve()

call = RDSDatabaseConnector(credentials)


call.database_connection()
