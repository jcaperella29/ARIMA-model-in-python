# SARIMA-model-in-python
This is python script for building a Seasonal -Autoregressive integrated moving average model . This example is predicting sales over several months.

First needed modules are imported , and scientific notation is removed.
Then the data is read in and examined.
Next, functions are built and used to add fields to the data that provide the year and month
Then  we aggregate Sales Quantity for each month
Next we use the melt function to convert the matrix of aggretated data into a single column
Then the total sales quanity per month is visualized.
Then the best parameters for the model are detrimined  after a related function is built.
After that the model is tuned with the best parameters and the predicitons are made
Then  the forecasts are then made into a dataframe along with the related month for each prediciton. 
The dataframe is then exported as a CSV file.
Lastly, the model accuracy is measured and a plot displaying the predictions for the months is created
