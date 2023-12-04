# Import necessary modules.
import missingno as msno


import plotly.express as px


import seaborn as sns


class Plotter:
    """
    Initialise the class for visualising data insights.

    Attributes:
        table (Pandas dataframe): specified dataframe to be visualised.
    """
    def __init__(self, table):
        """
        See help(Plotter) for accurate signature.
        """
        self.table = table

    def missing_data(self):
        """
        Generate a matrix of values within a specified dataframe.
        Returns:
            Matplotlib AxesSubplot object: matrix object representing present and missing values.
        """
        return msno.matrix(self.table)

    def pair_plot(self):
        """
        Generate a pair-plot of the dataframe.
        Returns:
            Grid: grid of scatterplots based on inputted dataframe.
        """
        return sns.pairplot(self.table)
    
    def correlation(self):
        """
        Generates correlation matrix of dataframe.
        Returns:
            matrix: a matrix of correlation scores between combinations of all columns within the dataframe.
        """
        numeric_columns = self.table.select_dtypes(include=['number'])
        return px.imshow(numeric_columns.corr(), aspect='equal', title='Correlation Heatmap', text_auto=True)
        