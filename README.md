# Trading Bot! 

This is an algorithm that implements the "pullback trading strategy" by Larry Connors. 

The Rules of the strategy are:

* Entry point: 
    - The stock price must be above the 200-day Moving Average
    - 10-period RSI(Relative strength index) below 30
* Exit point:
    - 10-period RSI above 40 or after 10 trading days

The algorithm executes trades on paper money by using alpaca's RESTful API. My algorithm datamines values from yahoo finance using pandas data reader to calculae moving average and RSI values.
