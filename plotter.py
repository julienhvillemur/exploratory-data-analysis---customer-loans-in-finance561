# Import necessary modules.
import missingno as msno

import seaborn as sns

class Plotter:
    """
    Initialise the class for visualising data insights.
    """
    def __init__(self, table):
        self.table = table

    def missing_data(self):
        return msno.matrix(self.table)

    def pair_plot(self):
        return sns.pairplot(self.table)
        