# Data analysis project

# Our project is titled **A visuel representation of The Purchasing Power Parity** 
# Purchasing Power Parity is a theory which states that fluctuations in prices between countries that heavily trade with eachother should be offset by the exchange rate between said countries. The reason why this should hold is, that if prices are lower in one country compared to the other, consumers from the country with higher prices would buy foreign products leading to a depreciation in their own exchange rate, until the price differences in the two countries would be levelled. 

# we will examine this by importing data from FRED (Federal Reserve Economic Data) and plotting consumer prices against exchange rates. we will plot the inflation rates against the exchange rates for the country sets (USA/Canada) and (USA/UK). According to the theory presented above, we should be able to see a correlation between inflation rates and exchange rates. 

# the results can be seen by running our Notebook [dataproject.ipynb] 


# We apply the following datasets from FRED 

1. Dataset containing consumer prices for all items for Canada (*https://fred.stlouisfed.org/series/CPALTT01CAA657N*)
2. Dataset containing consumer prices for all items for USA (*https://fred.stlouisfed.org/series/CPALTT01USA659N*)
3. Dataset containing consumer prices for all items for UK (*https://fred.stlouisfed.org/series/CPALTT01GBA659N*)
4. Dataset containing exchange rates between Canadian Dollar and US Dollar (*https://fred.stlouisfed.org/series/AEXCAUS*)
5. Dataset containing exchange rates between US Dollar and UK Pound Sterling (*https://fred.stlouisfed.org/series/AEXUSUK*)

**Dependencies:** Apart from a standard Anaconda Python 3 installation, the project requires the following installations:

``pip install matplotlib-venn``