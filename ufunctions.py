#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
from datetime import date
import pandas as pd


# In[2]:


def GetQuote(ticker="GME",start = "2018-01-01" ,end=str(date.today())):
    """
    """
    if not isinstance(ticker,str):
        raise Exception('String input expected')
    if not isinstance(start,str):
        raise Exception('String input expected')
    if not isinstance(end,str):
        raise Exception('String input expected')
        
    df = yf.download(ticker, start, end)
    
    return df


# In[39]:


def RelativeStrengthIndex(data, num=14):
    
    """
    """
    
    if not isinstance(data,pd.core.frame.DataFrame):
        raise Exception('DataFrame input expected')
    if not isinstance(num, int):
        raise Exception('Integer input expected')
    if num < 7 or num > 21:
        raise Exception('Unusual numeric input detected')
    if (num > len(data)):
        raise Exception('Insufficient data for calculation')
        

    data_keys=list(data.index)
    data_list=list(data['Adj Close'])
    
    
    result = {}
    last_price = -1
    gains_losses_list = []
    for x in range(len(data_list)):
        if (last_price != -1):
            diff = round((data_list[x] - last_price), 2)
            
            if (diff > 0):
                gains_losses = [ data_list[x], diff, 0 ]
            elif (diff < 0):
                gains_losses = [ data_list[x], 0, abs(diff) ]
            else:
                gains_losses = [ data_list[x], 0, 0 ]
            
            gains_losses_list.append(gains_losses)
        sum_gains = 0
        sum_losses = 0
        avg_gains = 0
        avg_losses = 0 
        if (x == num):
            series = gains_losses_list[-num::]
        
            for y in series:
                sum_gains += y[1]
                sum_losses += y[2]
            avg_gains = sum_gains / num
            avg_losses = sum_losses / num
            rs = avg_gains / avg_losses
            rsi = 100 - (100 / (1 + rs))
            last_gain_avg = avg_gains
            last_loss_avg = avg_losses
            result[data_keys[x]] = round(rsi, 2)
        if (x > num):
            current_list = gains_losses_list[-1::]
            current_gain = current_list[0][1]
            current_loss = current_list[0][2]
            current_gains_avg = (last_gain_avg * (num - 1) + current_gain) / num
            current_losses_avg = (last_loss_avg * (num - 1) + current_loss) / num
            rs = current_gains_avg / current_losses_avg
            rsi = 100 - (100 / (1 + rs))
            last_gain_avg = current_gains_avg
            last_loss_avg = current_losses_avg
            result[data_keys[x]] = round(rsi, 2)    
      
        last_price = data_list[x]
    
    result = pd.DataFrame(result.items(), columns=['Date', "RSI"+str(num)])
    result.set_index('Date',inplace=True)
        
    return result


# In[49]:


def macdIndex(data,shortSpan=12,longSpan=26,singalSpan=9):
    
    """
    
    """
    #Calculate the MACD and Signal Line indicators
    #Calculate the Short Term Exponential Moving Average
    ShortEMA = data.Close.ewm(span=shortSpan, adjust=False).mean() #AKA Fast moving average
    #Calculate the Long Term Exponential Moving Average
    LongEMA = data.Close.ewm(span=longSpan, adjust=False).mean() #AKA Slow moving average
    #Calculate the Moving Average Convergence/Divergence (MACD)
    MACD = ShortEMA - LongEMA
    #Calcualte the signal line (exp weighted)
    signal = MACD.ewm(span=singalSpan, adjust=False).mean()
    
    signal = signal.to_frame()
    signal.columns = ['SigMACD_'+str(shortSpan)+"_"+str(longSpan)+"_"+str(singalSpan)]
    MACD = MACD.to_frame()
    MACD.columns = ['MACD']
    
    
    return signal#,MACD


# In[53]:


# df = GetQuote()
# RSI_TEST= RelativeStrengthIndex(df, 14)
# RSI_TEST.head()
# MACD_TEST = macdIndex(df)
# MACD_TEST.tail()


# In[ ]:




