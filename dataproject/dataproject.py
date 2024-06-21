import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from matplotlib_venn import venn2
from scipy import stats
import pandas_datareader 
import datetime

class dataproject:
    def import_data():
        #Importing data form FRED

        #CPI data (Growth rate previous period (year), Not Seasonally Adjusted)
        CPI_CAN = 'CPALTT01CAA657N'
        CPI_USA = 'CPALTT01USA659N'
        CPI_UK = 'CPALTT01GBA659N'

        # Exchange rate 
        EX_CAN = 'AEXCAUS' #(Canadian Dollars to One U.S. Dollar, Not Seasonally Adjusted)
        EX_UK = 'AEXUSUK' #(U.S. Dollars to One U.K. Pound Sterling, Not Seasonally Adjusted)
        

        # Need first to encode dates in a python friendly to specify the length of the desired time period. 
        # Use the datetime module - it is the general way to handle dates in python. 
        start = datetime.datetime(1990,1,1)
        end = datetime.datetime(2020,1,1)
        timespan = end - start # We can investigate the precise time span by just subtracting to time variables.

        # Call the FRED api using pandas_datareader 
        inflation = pandas_datareader.data.DataReader([CPI_USA, CPI_UK, CPI_CAN], 'fred', start, end)
        inflation = inflation.rename(columns = {'CPALTT01USA659N':'CPI_USA','CPALTT01GBA659N':'CPI_CA','CPALTT01CAA657N':'CPI_UK'})

        # Call the FRED api using pandas_datareader 
        exchange = pandas_datareader.data.DataReader([EX_UK, EX_CAN], 'fred', start, end)
        exchange = exchange.rename(columns = {'AEXUSUK':'US-UK_exchange_rate','AEXCAUS':'CAN-US_exchange_rate'})
        exchange['US-UK_exchange_rate'] = 1 / exchange['US-UK_exchange_rate']

        return exchange, inflation
    
    def merge_outer(inflation, exchange):

        ppp = pd.merge(inflation, exchange, how = 'outer', on = ['DATE']);

        return ppp
    
    def ppp_pct_diff(ppp):

        ppp['CA_pct_dif_from_USA_CPI'] = ((ppp.CPI_CA-ppp.CPI_USA) / ppp.CPI_USA) *10 # the pct. difference between inflation in canada and USA
        ppp['UK_pct_dif_from_USA_CPI'] = ((ppp.CPI_UK-ppp.CPI_USA) / ppp.CPI_USA) *10 #the pct. difference between inflation in UK and USA
        ppp['US-UK_exchange_rate_DIF'] = (ppp['US-UK_exchange_rate'].diff() / ppp['US-UK_exchange_rate'].shift(1)) * 100 #tjek vejen
        ppp['CAN-US_exchange_rate_DIF'] = (ppp['CAN-US_exchange_rate'].diff() / ppp['CAN-US_exchange_rate'].shift(1)) * 100 #tjek vejen

        return ppp
    
    def filtered_ppp(ppp):


        # Calculate z-scores for each data point
        outlier_columns = ['CA_pct_dif_from_USA_CPI', 'UK_pct_dif_from_USA_CPI']
        z_scores = stats.zscore(ppp[outlier_columns])
        #print(z_scores)

        # Define a threshold for z-score
        threshold = 3  # Adjust this threshold as needed

        # Filter out rows where the absolute z-score exceeds the threshold
        filtered_ppp = ppp[((z_scores < threshold) & (z_scores > -threshold)).all(axis=1)] # removing for outliers
        filtered_ppp = filtered_ppp.drop(filtered_ppp.index[0]) #removing the first row 
        numbers_of_obs_before = ppp.describe().loc['count']
        numbers_of_obs_after = filtered_ppp.describe().loc['count']

        return filtered_ppp, numbers_of_obs_before, numbers_of_obs_after 
    
    def graphical_ppp(filtered_ppp):
        
        # Extract x and y values from the filtered dataset
        filtered_pct_dif_infl_UKUS = filtered_ppp['UK_pct_dif_from_USA_CPI']
        filtered_pct_dif_ex_UKUS = filtered_ppp['US-UK_exchange_rate_DIF'] 
        filtered_pct_dif_infl_CAUS = filtered_ppp['CA_pct_dif_from_USA_CPI']
        filtered_pct_dif_ex_CAUS = filtered_ppp['CAN-US_exchange_rate_DIF']
        filtered_ppp['x_diagonal'] = np.linspace(-20, 20, 28)
        filtered_ppp['y_diagonal'] = filtered_ppp['x_diagonal']

        return filtered_ppp, filtered_pct_dif_infl_UKUS, filtered_pct_dif_ex_UKUS, filtered_pct_dif_infl_CAUS, filtered_pct_dif_ex_CAUS 
    
    def five_year_average(ppp):

        # Define the time intervals
        intervals = [
            (ppp.index[0], ppp.index[4]),
            (ppp.index[5], ppp.index[9]),
            (ppp.index[10], ppp.index[14]),
            (ppp.index[15], ppp.index[18]),
            (ppp.index[19], ppp.index[22]),
            (ppp.index[23], ppp.index[28])
        ]

        # Create an empty list to store the mean values for each interval
        mean_values = []

        mean_year_mean_UK_pct_dif_from_USA_CPI = []
        mean_year_mean_CA_pct_dif_from_USA_CPI = []
        mean_year_mean_US_UK_exchange_rate_DIF = []
        mean_year_mean_CAN_US_exchange_rate_DIF = []

        # Iterate over the intervals
        for interval in intervals:
            start_date, end_date = interval
            
            # Filter the DataFrame for the current interval
            filtered_interval = ppp.loc[start_date:end_date]
            
            
            # Calculate the mean for the current interval
            five_year_mean_UK_pct_dif_from_USA_CPI = filtered_interval['UK_pct_dif_from_USA_CPI'].mean()
            five_year_mean_CA_pct_dif_from_USA_CPI = filtered_interval['CA_pct_dif_from_USA_CPI'].mean()
            five_year_mean_US_UK_exchange_rate_DIF = filtered_interval['US-UK_exchange_rate_DIF'].mean()
            five_year_mean_CAN_US_exchange_rate_DIF = filtered_interval['CAN-US_exchange_rate_DIF'].mean()


            # Append the mean value to the list
            mean_year_mean_UK_pct_dif_from_USA_CPI.append(five_year_mean_UK_pct_dif_from_USA_CPI)
            mean_year_mean_CA_pct_dif_from_USA_CPI.append(five_year_mean_CA_pct_dif_from_USA_CPI)
            mean_year_mean_US_UK_exchange_rate_DIF.append(five_year_mean_US_UK_exchange_rate_DIF)
            mean_year_mean_CAN_US_exchange_rate_DIF.append(five_year_mean_CAN_US_exchange_rate_DIF)

        return mean_year_mean_UK_pct_dif_from_USA_CPI, mean_year_mean_CA_pct_dif_from_USA_CPI, mean_year_mean_US_UK_exchange_rate_DIF, mean_year_mean_CAN_US_exchange_rate_DIF

        # Print the mean values for each interval
        #print(mean_year_mean_UK_pct_dif_from_USA_CPI, mean_year_mean_CA_pct_dif_from_USA_CPI, mean_year_mean_US_UK_exchange_rate_DIF, mean_year_mean_CAN_US_exchange_rate_DIF)


def keep_regs(df, regs):
    """ Example function. Keep only the subset regs of regions in data.

    Args:
        df (pd.DataFrame): pandas dataframe 

    Returns:
        df (pd.DataFrame): pandas dataframe

    """ 
    
    for r in regs:
        I = df.reg.str.contains(r)
        df = df.loc[I == False] # keep everything else
    
    return df