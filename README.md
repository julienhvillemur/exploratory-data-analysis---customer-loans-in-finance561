# Exploratory Data Analysis - Customer Loans In Finance

## Description:
The purpose of this project is to perform exploratory data analysis of sample customer loans data. This repository was created to provide an end to end system for handling, transforming and analysing large customer loans datasets. This will allow users to efficiently retrieve such datasets from RDS databases, remove or impute specific datapoints in preparation for analysis and apply a wide range of python methods to gain data insights.

Customer loan data in finance often forms large datasets, which require specific datahandling methods in order to gain desired insights about the data. Within this repository are multiple scripts which are used to handle, transform and analyse customer loans data. Therefore, this project removes the need of users to create scripts from scratch or use unoptimised software for their respective datasets.

Multiple methods of imputation are used in this project in order to handle the sizable proportion of null values often found in datasets. Furthermore, in order to further analysis such as via machine learning, advanced methods have been applied to further transform the data.

Post-transformation analysis has been performed in this project to characterise the type of customers listed in the sample dataset and to determine the impact of funding customer loans for the finance company.

There are a wide range of methods written specifically for this project and they provide both capacity for large datasets and flexibility to carry out various forms of data analysis.

## Installation:
Before runing the scripts in this repository, multiple python packages must be installed. Using `pip install <package>` install the following packages: `datetime`, `matplotlib`, `missingno`, `plotly`, `numpy`, `scipy`, `seaborn`, `sklearn`, `sqlalchemy`, `pandas` and `pyyaml`. You must then create a `credentials.yaml` file and input all of your user information for connection to the RDS database. Then the first file you must then run is `db_connector.py` in order to retrieve the customer loans dataset using your credentials. Run this file in your python interpreter; this will return and save the `loan_payments.csv` file within the same directory as the `db_connector.py` file. Once the customer loans data is visible in your directory you can continue on to use the .ipynb files contained within this repository.

## Usage instructions:
### Part 1 - Data Transformation
After following the installation instructions, run the `data_transformation.py` file in order to commence customer loan data transformation. This file makes use of the .py files contained within this project by importing methods for data retrieval, data analysis, transformation and visualisation. The .csv file saved during use of `db_connector.py` is then loaded into the notebook as a pandas dataframe. Methods imported from `data_transform.py` are then used to standardise the data in preparation for this project. Using the `DataFrameInfo` class, initial insights are made to understand the extent and dispersion of missing values within the data. This allows from the categorisation of data in preparation for imputation and removal with the `DataFrameTransform` class. After handling the missing data, the change to the dataframe is visualised via generate of a missing data matrix in the `missing_data()` method.

Further transformations are then performed to handle data skew and outliers. The skew is determined by using the `column_skew()` method, which returns a pandas series with skew scores and associated column names. This is then passed into the `yeojohnson_transform()` method to iterate through and transform data above a skew value of 1. The method then plots the transformed data within a histogram and returns the transformed dataframe. The code used to acheive this transformation is found below: ```for column, skew in skew_table.items():
            if skew > 1:  
                yeojohnson_data = self.table[column]
                yeojohnson_data = stats.yeojohnson(yeojohnson_data)
                yeojohnson_data= pd.Series(yeojohnson_data[0])
                self.table[column] = yeojohnson_data
                plot=sns.histplot(yeojohnson_data,label="Skewness: %.2f"%(yeojohnson_data.skew()))
                plot.legend()
        return self.table```
`skew_table` here refers to the data series of skew values previously generated and `self.table` refers to the customer loans dataset passed into the class. The final stages of the data transformation work include imputation of outliers (z-scores >3) with the median and dropping overly correlated columns in the dataset. A subeset of columns with high correlation scores are selected for reduced impact in potential future machine learning. At this stage, the transformed dataset is therefore ready for further analysis via machine learning.

### Part 2 - Exploratory Data Analysis


## File structure:

## Licence
