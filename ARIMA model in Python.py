
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

 
# Suppressing scientific notation and reading in the data
np.set_printoptions(suppress=True)
 
StoreSalesData=pd.read_excel("  user path /Super-Store-Sales-data.xls")
StoreSalesData.head()
#examining the data
StoreSalesData.info()

StoreSalesData.nunique()

#getting needed column
# Function to get month from a date
def Function_get_month(inpDate):
    return(inpDate.month)
 
# Function to get Year from a date
def Function_get_year(inpDate):
    return(inpDate.year)
 
 
# Creating new columns
StoreSalesData['Month']=StoreSalesData['Order Date'].apply(Function_get_month)
StoreSalesData['Year']=StoreSalesData['Order Date'].apply(Function_get_year)
 
StoreSalesData.head()


# Checking unique values in Year and Month Columns
print("Unique Values in Year Column: ", StoreSalesData['Year'].sort_values().unique())
print("Unique Values in Month Column: ", StoreSalesData['Month'].sort_values().unique())


# Aggregating the sales quantity for each month for all categories
pd.crosstab(columns=StoreSalesData['Month'],
            index=StoreSalesData['Year'],
            values=StoreSalesData['Quantity'],
            aggfunc='sum')


# Converting the crosstab data into one single column for Time Series
pd.crosstab(columns=StoreSalesData['Year'],
            index=StoreSalesData['Month'],
            values=StoreSalesData['Quantity'],
            aggfunc='sum').melt()

#Visualizing the Total sales Quantity per month


SalesQuantity=pd.crosstab(columns=StoreSalesData['Year'],
            index=StoreSalesData['Month'],
            values=StoreSalesData['Quantity'],
            aggfunc='sum').melt()['value']
 
MonthNames=['Jan','Feb','Mar','Apr','May', 'Jun', 'Jul', 'Aug', 'Sep','Oct','Nov','Dec']*4
 
# Plotting the sales
%matplotlib inline
SalesQuantity.plot(kind='line', figsize=(16,5), title='Total Sales Quantity per month')
# Setting the x-axis labels
plotLabels=plt.xticks(np.arange(0,48,1),MonthNames, rotation=30)

SalesQuantity.values




# Decomposing the Sales numbers in the Time Series data
series = SalesQuantity.values
result = seasonal_decompose(series, period=12)
#print(result.trend)
#print(result.seasonal)
#print(result.resid)
#print(result.observed)
result.plot()
CurrentFig=plt.gcf()
CurrentFig.set_size_inches(11,8)
plt.show()

# Creating the function to find best values of p,d,q for SARIMA
def FunctionTuneArima(inpData, p_values, d_values, q_values, 
                      seasonal_p_values, seasonal_d_values, seasonal_q_values,cycle):
    # Supressing warning messages
    import warnings
    warnings.filterwarnings(action='ignore')
    
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    # Fitting the model for each set of values passed
    
    # Creating an empty data frame to store
    Results=pd.DataFrame()
    
    # Trying the values
    for p_value in p_values:
        for d_value in d_values:
            for q_value in q_values:
                for seasonal_p_value in seasonal_p_values:
                    for seasonal_d_value in seasonal_d_values:
                        for seasonal_q_value in seasonal_q_values:
                            
                            try:
                                model = SARIMAX(inpData, 
                                    order=(p_value,d_value,q_value), 
                                    seasonal_order =(seasonal_p_value, 
                                                     seasonal_d_value,
                                                     seasonal_q_value,
                                                     cycle))
                                model_fit=model.fit(disp=False)
                                pred = model_fit.predict(0, len(inpData))
                                Acc=100- np.mean(abs(pred-inpData)/inpData*100)
                                
                                Results=pd.concat([Results,pd.DataFrame([[p_value,
                                                                   d_value,
                                                                   q_value,
                                                                   seasonal_p_value,
                                                                   seasonal_d_value,
                                                                   seasonal_q_value,
                                                                   Acc]],
                                                                   columns=["p","d","q",
                                                                           "seasonal_p",
                                                                           "seasonal_d",
                                                                           "seasonal_q",
                                                                           "Accuracy"
                                                                           ] )])
 
                            except:
                                pass
    return(Results)

# Calling the function to get the best values
# This can take some time because there are multiple combinations!
# Cycle=12 because this is monthly data
ResultsData=FunctionTuneArima(inpData=SalesQuantity,
                  p_values=[0,1], 
                  d_values=[0,1], 
                  q_values=[1,10], 
                  seasonal_p_values=[1,2],                                       
                  seasonal_d_values=[0], 
                  seasonal_q_values=[0],
                  cycle=12
                 )

# Sorting the results to get the 10 best combinations
ResultsData.sort_values('Accuracy', ascending=False).head(10)

# Importing the algorithm
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')
 
 
# Train the model on the full dataset 
SarimaxModel = SARIMAX(SalesQuantity,  
                        order = (1, 0, 10),  
                        seasonal_order =(2, 0, 0, 12))
 
 # Fitting the Time series model on the data
SalesModel = SarimaxModel.fit(disp=False)
  
# Forecast for the next 6 months
FutureMonths=6
forecast = SalesModel.predict(start = 0,
                          end = (len(SalesQuantity)) + FutureMonths,
                          typ = 'levels').rename('Forecast')
print("Next Six Month Forecast:\n",forecast[-FutureMonths:])

forecast_df=pd.DataFrame(forecast[-FutureMonths:])
forcast_df_with_months=forecast_df.assign(Months =MonthNames[0:FutureMonths])
forcast_df_with_months.to_csv(    user path /Time_series_results")

 
# Plot the forecast values
SalesQuantity.plot(figsize = (18, 5), legend = True, title='Time Series Sales Forecasts')
forecast.plot(legend = True, figsize=(18,5))
 
# Measuring the Training accuracy of the model
MAPE=np.mean(abs(SalesQuantity-forecast)/SalesQuantity)*100
print('#### Accuracy of model:', round(100-MAPE,2), '####')
 

 
# Printing month names in X-Axis
PlotMonthNames=MonthNames+MonthNames[0:FutureMonths]
plotLabels=plt.xticks(np.arange(0,len(PlotMonthNames),1),PlotMonthNames, rotation=30)


#orginal code was from https://thinkingneuron.com/time-series-forecasting-in-python-for-superstore-dataset/ ,I made changes to allow the user to export the results.
