import sys
import requests        
import pandas as pd   
from datetime import datetime,timedelta,date
from dotenv import dotenv_values
from pymongo import MongoClient
import json

class Crypto:
    df = pd.DataFrame()
    
    def __init__(self,symbol):
        self.symbol = symbol

    def str_to_epoch_ms(self,date:str):
        """ convert date string to epoch time in miliseconds """
        return int(datetime.strptime(date,'%Y-%m-%d').timestamp()*1000)
    
    def data_update (self):
        """ update today's data untile now
        
        Parameters
        ----------
        symbol : str 
        symbol supported by Binance API. 
        """
        start = date.today()
        end = start + timedelta(days=1)
        self.df = self.df.append(self.data_to_df(
            start.isoformat(),end.isoformat()))
    
    def data_to_df (self,start_time:str,end_time:str):
        """ Get data from Binance API and convert it to a pandas data frame
        numbers of candles are limited to 1500 per request
    
        Parameters
        ----------
        symbol : str 
        symbol supported by Binance API.
        start_time : str
            start date for retriving data  format: 2020-12-30.
        end_time : str
            end date for retriving data: 2020-12-30.
    
        Raises
        ------
        SystemExit
            The end date must be larger than the start date.
            
        Returns
        -------
        df : pandas data frame
            converted API response to a data frame.
        """
        start = self.str_to_epoch_ms(start_time)
        end = self.str_to_epoch_ms(end_time)
        
        if end<start:
            raise SystemExit("End date must be larger than start date")
            
        url = 'https://fapi.binance.com/fapi/v1/klines'
        params = {
        'symbol':str(self.symbol),
        'interval':'1m',
        'startTime':start,
        'endTime': end,
        'limit':'1500'
        }
        
        try:
            request = requests.get(url,params=params)
        except requests.exceptions.RequestException as exp :
            raise SystemExit(exp)
            sys.exit(1)
        
        data = request.json()
        
        if type(data) == dict:
            raise SystemExit(f"error code: {data['code']}\nmessage : \
                {data['msg']}")
        try:
            data[0]
        except IndexError :
            raise SystemExit("there is no response from your request")
            sys.exit()
            
        if len(data) == 1500:
            print("Warning :\nthe limit rate for binance API is 1500 ")
            
        df = pd.DataFrame(data)
        df.columns = ['OpenTime','Open','High','Low','Close','Volume',
                    'CloseTime','QuoteVolume','TradesNumber','TakerBaseVolume',
                    'TakerQuoteVolume','Ignore']
        df.index = df.OpenTime
        return df


    def collect_data (self, start_date:str, end_date:str):
        """ Split request with large interval time to smaller request in order to 
        over come binance api limitaion 
    
        Parameters
        ----------
        start_time : str
            start date for retrieving data  format: 2020-12-30.
        end_time : str
            end date for retrieving data: 2020-12-30.
        """
        date_range = pd.date_range(start_date,end_date)
        for i,day in enumerate(date_range):
            if len(date_range)>i+1:
                self.df = self.df.append(
                        self.data_to_df(day.strftime('%Y-%m-%d'),
                                    date_range[i+1].strftime('%Y-%m-%d')))
    
    def insert_to_mongo(self):
        """ insert data to mongoDB 
        """
        config = dotenv_values('/.env')
        client = MongoClient(
            config['MONGO_Host'],
            config['MONGO_Port'],
            username=config['MONGO_User'],
            password=config['MONGO_Password'])
        mycol = client[config['MONGO_DB']][self.symbol]
        self.df['_id']=self.df.OpenTime.astype(str)
        json_list = json.loads(json.dumps(list(self.df.T.to_dict().values())))
        mycol.insert_many(json_list) 


