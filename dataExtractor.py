#Pandas will help for the output.   
import pandas as pd
import numpy as np
#Using requests to get binance API.
import requests

class Extractor:
    def getData(self):
        def cleanOutput(tickerString):
            if tickerString[-4:] == 'USDT':
                return [tickerString.split('USDT')[0].lower(), 'usdt']
            elif tickerString[-3:] == 'ETH':
                return [tickerString.split('ETH')[0].lower(), 'eth']
            elif tickerString[-3:] == 'BTC':
                return [tickerString.split('BTC')[0].lower(), 'btc']
            elif tickerString[-3:] == 'BNB':
                return [tickerString.split('BNB')[0].lower(), 'bnb']
            return np.nan

        #Working with the data.
        api = 'https://api.binance.com/api/v1/ticker/24hr'
        data = pd.DataFrame(requests.get(api).json())
        data['symbol'] = data.apply(lambda x: cleanOutput(x['symbol']), axis=1)
        data = data.dropna()
        data['base'] = data.apply(lambda x: x['symbol'][0], axis=1)
        data['quote'] = data.apply(lambda x: x['symbol'][1], axis=1)
        data['quote'] = data['quote'].str.replace('usdt', 'usd')
        data = data.rename(index=str, columns={'askPrice': 'ask','bidPrice': 'bid','lastPrice': 'price'})
        columns = ['ask', 'bid', 'price', 'volume']
        data['exchange'] = 'binance'
        data[columns] = data[columns].astype(float)
        data['spread'] = data.ask - data.bid
        columns.extend(['base', 'quote', 'spread', 'exchange'])
        data = data[columns]
        data['ticker'] = data.apply(lambda x: x['base'] + '-' + x['quote'], axis=1).tolist()
        data = data[['base', 'quote', 'exchange', 'price', 'ask', 'bid', 'spread', 'volume', 'ticker']].set_index('ticker')
        return data


dataFrame = Extractor().getData()
print(dataFrame.head())   
#using pandas .to_csv() methode to convert dataframe into a csv file.            
print(dataFrame.to_csv('data.csv',';'))