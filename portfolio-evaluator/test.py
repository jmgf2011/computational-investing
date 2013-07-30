import portfolio_evaluator
import datetime

start_time = datetime.date(2011, 1, 1) #January 1st 2011
end_dtime = datetime.date(2011, 12, 31) #Dec 31st 2011

symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']
allocations = [0.4, 0.4, 0.0, 0.2]

# Display data about the indicated companies over the year 2011
portfolio_evaluator.simulate(start_time, end_time, symbols, allocations)
