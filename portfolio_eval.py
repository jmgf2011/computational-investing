import numpy
import math

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

#inputs: start date, end datlle, symbols for equities, equity allocations
#output: Standard deviation of daily returns of total portfolio, avg. daily returns of total portfolio, sharpe ratio, cumulative return of total portfolio.
def simulate(start_date, end_date, equities, allocations):
    d_data = get_data(start_date, end_date, equities)
    na_price = d_data['close'].values
    daily_returns = get_daily_returns(na_price)
    total_daily_returns = get_total_daily_returns(daily_returns, allocations)
    standard_dev_daily_returns_total_portf = numpy.std(total_daily_returns, axis=0)
    avg_daily_total_return = numpy.mean(total_daily_returns)
    #TODO: Probably not calculating this correctly.
    cumulative_total_daily_returns = get_cumulative_total_daily_returns(total_daily_returns)
    sharpe_ratio = math.sqrt(252)*(avg_daily_total_return/standard_dev_daily_returns_total_portf)
    print("Symbols:" + str(equities))
    print("Allocations: " + str(allocations))
    print ("Sharpe Ratio: " + str(sharpe_ratio))
    print ("Volatility (stdev of daily returns): " + str(standard_dev_daily_returns_total_portf)) 
    print ("Average Daily Return: " + str(avg_daily_total_return))
    print ("Cumulative Return: " + str(cumulative_total_daily_returns))


def get_cumulative_total_daily_returns(total_daily_returns):
    t = len(total_daily_returns)
    return daily_cum_ret(t, total_daily_returns)

#OBOBS EVERYWHERE
def daily_cum_ret(t, total_daily_returns):
    
    if t == 1:
        return 1
    #print ('t: ' + str(t))
    #print('len of total daily returns: ' + str(len(total_daily_returns)))
    return (daily_cum_ret(t-1, total_daily_returns) * (1 + total_daily_returns[t-1]))

# Get the list of share prices for each company over the specified date range.
def get_data(start_date, end_date, equities):
    # Read data available at the close of the day (4pm).
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(start_date, end_date, dt_timeofday)

    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, equities, ls_keys)
    #print("ldf_data: ")
    #sprint(ldf_data)
    d_data = dict(zip(ls_keys, ldf_data))
    return d_data


def normalize_data(na_price):
    return na_price/na_price[0, :]

# Get the total return of each company, each day.
def get_daily_returns(na_price):
    na_normalized_price = normalize_data(na_price)
    na_rets = na_normalized_price.copy()
    return tsu.returnize0(na_rets)

# Returns a list of the total return for each day
def get_total_daily_returns(daily_returns, allocations):
    # Create a list of zeroes having the length of the number of days in the range we are looking at.
    daily_returns_total_portf = []
    
    for daily_return in daily_returns:
        i = 0
        curr_sum = 0
        for return_by_company in daily_return: 
            curr_sum += return_by_company * allocations[i]
            i += 1
        daily_returns_total_portf.append(curr_sum) 
    return daily_returns_total_portf
            
