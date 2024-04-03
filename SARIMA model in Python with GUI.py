
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

import PySimpleGUI as sg
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from tkinter import * 
from tkinter.ttk import *
import copy
import os
import shutil
import os.path
import glob



def Build_and_use_SARIMA(excel_path):
# Suppressing scientific notation and reading in the data
    np.set_printoptions(suppress=True)
 
    StoreSalesData=pd.read_excel(excel_path)
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
 

    SalesQuantity.values




# Decomposing the Sales numbers in the Time Series data
    series = SalesQuantity.values
    result = seasonal_decompose(series, period=12)
#print(result.trend)
#print(result.seasonal)
#print(result.resid)
#print(result.observed)
   

               

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

    forecast_df=pd.DataFrame(forecast[-FutureMonths:])
    forecast_df_with_months=forecast_df.assign(Months =MonthNames[0:FutureMonths])
    


         
 

 
# Measuring the Training accuracy of the model
    MAPE=np.mean(abs(SalesQuantity-forecast)/SalesQuantity)*100
    print('#### Accuracy of model:', round(100-MAPE,2), '####')
    #forecast_df_with_months['accuracy']=round(100-MAPE,2)
    forecast_df_with_months['MAPE']=pd.Series()
    forecast_df_with_months.iloc[0,forecast_df_with_months.columns.get_loc('MAPE')]=round(100-MAPE,2)
    return(forecast_df_with_months)
 

 


sg.theme('Reddit')
layout =  [ [sg.Text( " Use a SARIMA model using Python"), sg.Input(),sg.FileBrowse(key="-IN-")],[sg.Submit()],[sg.Cancel()]]
        
newlayout = copy.deepcopy(layout)
window = sg.Window('Select and submit a excel  file containing your data', newlayout, size=(270*4,4*100))
event, values = window.read()

while True:
    event, values = window.read()
    print(event, values)
    
    if event == 'Cancel':
        break
    elif event == 'Submit':
        #results=analyze_list_of_images("im_path_list")
        #results
         excel_path= values["-IN-"]
         if excel_path:
    
            output =  pd.DataFrame(Build_and_use_SARIMA(excel_path))
         
            break
window.close()

def save_file():
            file = filedialog.asksaveasfilename(
                
            filetypes=[("csv file", ".cvs")],
            defaultextension=".csv",
            title='Save Output')
            results_file=output.to_csv(str(file))
            if file: 
                            fob=open(str(results_file),'w')
                            fob.write("Save results")
                            fob.close()
            else: # user cancel the file browser window
                        print("No file chosen")
       
if output is not None:  
           
        my_w = tk.Tk()
        my_w.geometry("400x300")  # Size of the window 
        my_w.title('Save results as a CVS')
        my_font1=('times', 18, 'bold')
        l1 = tk.Label(my_w,text='Save File',width=30,font=my_font1)
        l1.grid(row=1,column=1)
        
        b1 = tk.Button(my_w, text='Save', 
        width=20,command = lambda:save_file())
        b1.grid(row=2,column=1)
        
        b2=tk.Button(my_w, text="Quit", command=my_w.destroy)
        b2.grid(row = 3, column=1)
        my_w.mainloop() 
        
#orginal code was from https://thinkingneuron.com/time-series-forecasting-in-python-for-superstore-dataset/ ,I made changes to allow the user to export the results.