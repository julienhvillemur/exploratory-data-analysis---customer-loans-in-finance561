# Import necessary modules.
import matplotlib.pyplot as plt


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
        Generate correlation matrix of dataframe.
        Returns:
            Matrix: a matrix of correlation scores between combinations of all columns within the dataframe.
        """
        numeric_columns = self.table.select_dtypes(include=['number'])
        return px.imshow(numeric_columns.corr(), aspect='equal', title='Correlation Heatmap', text_auto=True)

    def bar_chart(self, loan_recoveries):
        """
        Generate a bar chart of the provided loan recovery percentages.
        Args:
            Dict: Key - type of loan recovery. Value - percentage amount recovered against the total fund.
        Returns:
            BarContainer: a bar chart presenting multiple loan recovery values.
        """
        categories = list(loan_recoveries.keys())
        percentages = list(loan_recoveries.values())
        plt.ylabel('Percentage')
        return plt.bar(categories, percentages, tick_label=categories)

    def line_graph(self, projected_loss, real_loss):
        """
        Visualise projected loss using line graph.
        Displays PyPlot of projected loss data.
        """
        months = [0, 60]
        loss = [0, projected_loss]
        real_loss_plot = [0, real_loss]
        plt.plot(months, loss, label='Projected Loss')
        plt.plot(months, real_loss_plot, label='Real Projected Loss')
        plt.xlabel('Months')
        plt.ylabel('Projected Loss')
        leg = plt.legend(loc='upper center')
        plt.show()
        
    def heat_map(self):
        return sns.heatmap(self.table[['loan_status', 'grade', 'purpose', 'home_ownership']].corr(), annot=True, cmap='coolwarm')