"""
Description:

In this implementation, I choosed fbprophet python module which greatly ease
my rest of implementation to predict facebook stock price data, thanks to facebook
data science team. Also I implemented few helper function to render respective web page
that can display predicted stock price data.
"""

"""
New used Python Modules:

pandas
fbprophet::Prophet
pandas_datareader.data:: web
flask
pathlib
itertools::zip_longest
"""

import pandas as pd
import numpy as np
import pandas_datareader.data as web
from fbprophet import Prophet
import datetime
from flask import Flask, render_template
from flask import request, redirect
from pathlib import Path
import datetime
import time
import os
import os.path
import csv
from itertools import zip_longest

app = Flask(__name__)

@app.after_request
def add_header(response):
    """
    Add headers to web browser such as Edge, Google chrome.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
    
@app.route("/")
# render fist page
def first_page():
    """
    stock = "Facebook"
    return render_template("plot.html", original = original_end, forecast = forecast_start, stock_tinker = stock)
    """
    tmp = Path("stat/prophet.png")
    tmp_csv = Path("stat/FB_stockData.csv")
    if tmp.is_file():
        os.remove(tmp)
    if tmp_csv.is_file():
        os.remove(tmp_csv)
    return render_template("index.html")

#function to get stock data using python module pandas
def facebook_stocks(symbol, start, end):
    return web.DataReader(symbol, 'facebook', start, end)

#helper function to collect historical data
def get_historical_stock_price(stock):
    print ("acquiring historical stock prices for stock ", stock)
    
    #get last 365 days stock data for facebook
    startDate = datetime.datetime(2017, 01, 01)
    endDate = datetime.datetime(2018, 01, 01)
    stockData = facebook_stocks(stock, startDate, endDate)
    return stockData

@app.route("/plot" , methods = ['POST', 'GET'] )
def main():
    if request.method == 'POST':
        stock = request.form['companyname']
        stData = get_historical_stock_price(stock)

        df = stData.filter(['Close'])
        df['ds'] = df.index
        #log transform the ‘Close’ variable to convert non-stationary data to stationary one.
        df['y'] = np.log(df['Close'])
        original_end = df['Close'][-1]

        # using python module fbprophet which is used to forecasting time series data
        model = Prophet()
        model.fit(df)

        # Number of days to predict stock price for
        n_days = 3
        future = model.make_future_dataframe(periods=n_days)
        forecast = model.predict(future)
        
        print (forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        
        #Prophet plots the observed values of time series (the black dots), the forecasted values (blue line)
        #and the uncertainty intervalsof our forecasts (the blue shaded regions).
        
        #make the vizualization a little better to understand
        df.set_index('ds', inplace=True)
        forecast.set_index('ds', inplace=True)
        
        visl_df = df.join(forecast[['yhat', 'yhat_lower','yhat_upper']], how = 'outer')
        visl_df['yhat_scaled'] = np.exp(viz_df['yhat'])

        close_data = visl_df.Close
        forecasted_data = visl_df.yhat_scaled
        date = future['ds']
        
        forecast_start = forecasted_data[-n_days]

        d = [date, close_data, forecasted_data]
        export_data = zip_longest(*d, fillvalue = '')
        with open('static/FB_stockData.csv', 'w', encoding="ISO-8859-1", newline='') as csvfile:
            wr = csv.writer(csvfile)
            wr.writerow(("Date", "Actual", "Forecasted"))
            wr.writerows(export_data)
        csvfile.close()

        return render_template("plot.html", original = round(original_end,2), forecast = round(forecast_start,2), stock_tinker = stock.upper())
    
if __name__ == "__main__":
    app.run(debug=True, threaded=True)
