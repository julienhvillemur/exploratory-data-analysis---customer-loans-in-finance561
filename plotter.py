# Import necessary modules.
import missingno as msno


import plotly.express as px


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
    
    def correlation(self):
        numeric_columns = self.table.select_dtypes(include=['number'])
        return px.imshow(numeric_columns.corr(), title='Correlation Heatmap')
        