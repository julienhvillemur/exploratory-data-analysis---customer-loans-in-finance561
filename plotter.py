# Import necessary modules.
import missingno as msno


class Plotter:
    """
    Initialise the class for visualising data insights.
    """
    def __init__(self, table):
        self.table = table

    def missing_data(self):
        msno.matrix(self.table)