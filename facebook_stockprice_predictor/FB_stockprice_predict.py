"""
Description:

This project dedicated to implement web based application in python environment, and whole environement has been set up with Flask.
In this project I programmatically collect last 365 days of facebook stock price data using python modules bs4::BeautifulSoup and
request and write to temporary csv file by using csv, Request module. Based on the data collected, opening price for requested time
period is predicted by using Logistic regression model by using sklearn::linear_model python module. confidence accuracy of logistic
regression and SGD classifier are implemented. For displaying the stock chart on respective web page, I used dygraph java scripts library.
Whenever the stock prediction for facebook stock completed, temporary historical data that collected from web API will be deleted.


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
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from bs4 import BeautifulSoup
from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score

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
        
    numFolds = 10
    kf = KFold(len(data_pool), numFolds, shuffle=True)
    X=data_pool["data"]
    Y=data_pool["target"]
    RegMod=[LogisiticRegression, SGDClassifier]
    params = [{}, {"loss": "log", 'n_iter':1000}]
    
    # use built it function zip() to return iterator ot tuples based on iterable object (list of parameter and diff Regression model)
    for params, RegMod in zip(params, RegMod):
        total=0
        for tr_idx, tst_idx in kf:
            train_X=X[tr_idx,:]; train_Y=Y[tr_idx]
            test_X=X[tst_idx,:];test_Y=Y[tst_idx,:]
        
            lin_model=linear_model.LogisticRegression()
            lin_model.fit(train_X, train_Y)
            predicted_price=lin_model.predict(test_X)
            total += accuracy_score(test_Y, predicted_price)
        accuracy = total / numFolds
        print "Accuracy score of {0}: {1}".format(RegMod.__name__, accuracy)
    return predicted_price[0][0],lin_model.coef_[0][0] ,lin_model.intercept_[0]

# Check if we got the historical data
if not get_historical_data(stock_data):
    print "input is missing !"
    sys.exit()
#print out stock prediction result
print (stock_prediction())
# whenever stock prediction is done, temp stock data can be deleted.
os.remove(File_Name)
