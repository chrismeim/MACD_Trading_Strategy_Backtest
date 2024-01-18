import yfinance as yf
import pandas as pd
import time

start_time = time.time()

tickers = ["AMZN","GOOG","MSFT"]
ohlcv_data = {}
for ticker in tickers:
    temp = yf.download(ticker, period = "1mo", interval="15m")
    temp.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = temp

def MACD(DF,a=12,b=26,c=9): #a,b,c determine the window that we have to calculate for the series
    df = DF.copy() #this dataframe will be changed, so we want the original to be in-tact
    df["ma_fast"] = df["Adj Close"].ewm(span = a, min_periods=a).mean()
    df["ma_slow"] = df["Adj Close"].ewm(span = b, min_periods=b).mean()
    df["macd"] = df["ma_fast"] - df["ma_slow"]
    df["signal"]= df["macd"].ewm(span = c, min_periods=c).mean()
    return df.loc[:,["macd","signal"]]


for ticker in ohlcv_data:
    ohlcv_data[ticker][["MACD","SIGNAL"]] = MACD(ohlcv_data[ticker])



return_dict = {}
daily_return = []
for ticker in tickers:
    stock = ohlcv_data[ticker]
    i = 25
    
    while (i < len(stock) - 1):
        i += 1
        if (stock.iloc[i][6] >= stock.iloc[i][7]) and (stock.iloc[i-1][6] < stock.iloc[i-1][7]):
            pt_start = stock.iloc[i][4]
            while (stock.iloc[i][6] >= stock.iloc[i][7]) and (i < len(stock)-1):
                pt_end = stock.iloc[i][4]
                i += 1
            pct_return = (pt_end - pt_start)/pt_start
            daily_return.append(pct_return)
            
        elif (stock.iloc[i][6] <= stock.iloc[i][7]) and (stock.iloc[i-1][6] > stock.iloc[i-1][7]):
            pt_start = stock.iloc[i][4]
            while (stock.iloc[i][6] <= stock.iloc[i][7]) and (i < len(stock)-1):
                pt_end = stock.iloc[i][4]
                i += 1
            pct_return = (pt_end - pt_start)/pt_start
            daily_return.append(pct_return)
    
    return_dict[ticker] = daily_return
    daily_return = []


end_time = time.time()
total_time = end_time - start_time
print(f"The total time was {total_time}")

for ticker in tickers:
    return_dict[ticker] = pd.DataFrame(return_dict[ticker])
    print(return_dict[ticker].sum())
    ((1+return_dict[ticker]).cumprod()-1).plot(title = f"Performance of MACD Trading Strategy {ticker}", xlabel = "Return",ylabel = "Time")

    


  



