## flask app for facebook stockpprice prediction
 Author: Jurat Shayiding
 Project created: 2017-11-20

This project dedicated to implement web based application in python environment, and whole environement has been set up with Flask.
In this project I programmatically collect last 365 days of facebook stock price data using python modules bs4::BeautifulSoup and 
request and write to temporary csv file by using csv, Request module. Based on the data collected, opening price for requested time 
period is predicted by using Logistic regression model by using sklearn::linear_model python module. confidence accuracy of logistic
regression and SGD classifier are implemented. For displaying the stock chart on respective web page, I used dygraph java scripts library. 
Whenever the stock prediction for facebook stock completed, temporary historical data that collected from web API will be deleted.
