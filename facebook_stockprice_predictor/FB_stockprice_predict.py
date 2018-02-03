"""
Description:

This project dedicated to implement web based application in python development
environment, and whole environement has been set up with Flask.
In this project I programmatically collect last 365 days of facebook stock price data
using python modules bs4::BeautifulSoup and request and write to temporary csv file.
based on the data collected, opening price for requested time period is predicted 
by using linear regression model by using sklearn::linear_model python module. 
Whenever the stock prediction for facebook stock completed, temporary historical data
that collected from web API will be deleted.


Python version used 3.6

Modules needed:

Used Python modules:


requests
bs4::BeautifulSoup
sklearn::linear_model
Pandas
Numpy
scikit-learn
time
datetime
csv
os
sys
"""


import os
import sys
import requests
import numpy as np
import time
import csv
import datetime
from sklearn import linear_model
from bs4 import BeautifulSoup

File_Name='FB_historical_stock_data.csv'

# retrive Facebook historical data for stock price prediction
def get_historical_data(stock_data):
    url='https://finance.yahoo.com/quote/FB/history?period1=1486076400&period2=1517612400&interval=1d&filter=history&frequency=1d'
    html_doc=requests.get(url, stream=True)
    if html_doc.status_code!=400:
        soup=BeautifulSoup(html_doc.content,'html.parser')
        div=soup.find(id="Col1-1-HistoricalDataTable-Proxy")
        table=div.select_one("table")
        headers = [th.text.encode("utf-8") for th in table.select("tr th")]
        with open(File_Name, "w") as f:
            wr = csv.writer(f)
            wr.writerows([[td.text.encode("utf-8") for td in row.find_all("td")] for row in table.select("tr + tr")])
        return True

# helper function for stock prediction of facebook analytics
def stock_prediction():
    data_pool=[]
    with open(File_Name) as fnc:
        for n, line in enumerate(fnc):
            if n!=0:
                str=line.split(',')[1]
            if str!="-":
                data_pool.append(float(line.split(',')[1]))
    data_pool=np.array(data_pool)
    
    def create_dataPools(data_pool):
        data_X=[data_pool[n+1] for n in range(len(data_pool)-2)]
        res=np.array(data_X), data_pool[2:]

    train_X=create_dataPools(data_pool)
    
    def predict_stock_price(dates, prices, train_X):
        lin_model=linear_model.LinearRegression()
        dates=np.shape(dates, (len(dates),1))
        prices=np.shape(prices, (len(prices),1))
        lin_model.fit(dates, prices)
        predicted_price=lin_model.predict(train_X)
        res= predicted_price[0][0],lin_model.coef_[0][0] ,lin_model.intercept_[0]
        return res
    # Check if we got the historical data
    if not get_historical_data(stock_data):
        print "input is missing !"
        sys.exit()
    #print out stock prediction result
    print (stock_prediction())
    # whenever stock prediction is done, temp stock data can be deleted.
    os.remove(File_Name)
