import sys
import requests        
import pandas as pd   
from datetime import datetime,timedelta,date
from dotenv import dotenv_values
from pymongo import MongoClient
import json
import time

class Crypto:
    """"""
    # Class attributes common to all instances
    _df = pd.DataFrame()
    _symbol = ""
    _config = dotenv_values('/.env')

    def set_symbol(self,symbol:str):
        """ set the symbol of the class
        Parameters
        ----------
        symbol : str 
            symbol supported by Binance API.
        """
        self._symbol = symbol
    
    def _progress(self,count, total, status=''):
        import sys
        """progress bar function developed by https://gist.github.com/vladignatyev
        parmeters: count, total, status
        ----------
        count : int
            current number of tasks
        total : int
            total number of task
        status : str
            status of the progress bar
        """ 
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.1 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        sys.stdout.flush()
    
    def _str_to_epoch_ms(self,date:str):
        """ convert date string to epoch time in miliseconds """
        str_data = str(date)
        return int(datetime.strptime(str_data,'%Y-%m-%d').timestamp()*1000)

    def _data_update (self,data_frame):
        """ update today's data untile now
        Parameters
        ----------
        symbol : str 
        symbol supported by Binance API.
        return : pandas data frame
        append new data to the data frame 
        """
        start = date.today()
        end = start + timedelta(days=1)
        data_frame = data_frame.append(self._data_to_df(start.isoformat(),
                                                end.isoformat()))
        return data_frame

    def _data_to_df (self,start_time:str,end_time:str):
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
        start = self._str_to_epoch_ms(start_time)
        end = self._str_to_epoch_ms(end_time)

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
            
        if len(data) == 1500:
            print("Warning :\nthe limit rate for binance API is 1500 ")
        df = pd.DataFrame(data)
        df.columns = ['OpenTime','Open','High','Low','Close','Volume',
                    'CloseTime','QuoteVolume','TradesNumber','TakerBaseVolume',
                    'TakerQuoteVolume','Ignore']
        df.index = df.OpenTime
        
        return df

    def _collect_data (self, start_date:str, end_date:str):
        """ Split request with large interval time to smaller request in
        order to over come binance api limitaion 
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
                    self._df = self._df.append(
                            self._data_to_df(day.strftime('%Y-%m-%d'),
                                        date_range[i+1].strftime('%Y-%m-%d')))
                    self._progress(i,len(date_range),status=f"{self.symbol} data is loading")
            if i % 50 == 0:
                time.sleep(2)

    def _mongo_connection(self):
        """ connect to mongoDB with credentials from .env file
        Returns:
            Mongo Client Oject
        """
        client = MongoClient(
            self._config['MONGO_Host'],
            int(self._config['MONGO_Port']),
            username=self._config['MONGO_User'],
            password=self._config['MONGO_Password'])
        return client

    def _insert_to_mongo(self):
        """ insert data to mongoDB
            read .env file to get mongoDB credentials
            create a new collection if it doesn't exist
        """
        client = self._mongo_connection() 
        try :
            client
        except Exception as exp:
            raise SystemExit(exp)
            
        mycol = client[self._config['MONGO_DB']][self.symbol]
        # Set the unique index using the open time
        self._df['_id']=self._df.OpenTime.astype(str)
        # First convert the dataframe to a list of dictionaries
        # then insert the list into the collection with json format 
        json_list = json.loads(json.dumps(list(self._df.T.to_dict().values())))
        try:
            # Ignore duplicate records
            mycol.insert_many(json_list , ordered=False)
        except Exception as exp:
            pass

    def load_crypto_data(self,symbol,start_date='2019-01-01',
                end_date=str(date.today()),
                interval='1T'):
        """load data from mongoDB and convert it to a pandas data frame
        with desire time frequency
        
        Parameters
        ----------
            start_date : str
                start date for retrieving data  format: 2020-12-30.
            end_date : str  
                end date for retrieving data: 2020-12-30
            interval : str
                interval time for retrieving data.
                default value is 1T (1 minute)
        """
        self.set_symbol(symbol)
        client = self._mongo_connection()
        mycol = client[self._config['MONGO_DB']][self.symbol]
        try :
            mycol
        except Exception as exp:
            raise SystemExit(exp)

        start = self._str_to_epoch_ms(start_date)
        end = self._str_to_epoch_ms(end_date)

        latest = int(self._get_latest_data())

        # check data exist in database
        if end > latest :
            self._get_data()

        # get interval data from mongoDB and convert it to a pandas data frame
        data = pd.DataFrame(list(mycol.find(
            {'_id':{'$gt': str(start),
                    '$lt':str(end)}})))
        
        # today data , append to database fetched data
        if end >= self._str_to_epoch_ms(str(date.today())) :       
            data = self._data_update(data)
        
        data = self._clean_data(data)
        
        return self._tf_maker(data,interval)
    
    def _clean_data (self,data):
        """transform data in data frame to classic candle stick with volume
        Parameters
        ----------
        df : pandas data frame
            data frame complete data of symbol.
        Returns
        -------
        pandas data frame
            clean classic candle stick with indexig date.
        """ 
        data.index = [datetime.fromtimestamp(x/1000) for x in data.OpenTime]
        data.index.name = 'Date'
        data['Open'] = pd.to_numeric(data['Open'],downcast="float")
        data['High'] = pd.to_numeric(data['High'],downcast="float")
        data['Low'] = pd.to_numeric(data['Low'],downcast="float")
        data['Close'] = pd.to_numeric(data['Close'],downcast="float")
        data['Volume'] = pd.to_numeric(data['Volume'],downcast="float")
        
        return data[['Open','High','Low','Close','Volume']]
    
    def _tf_maker(self,data,interval):
        """ transform data to desire time frequency 
            with candle stick and volume data pattern
        """
        offset =""" 
        Wronge Interval!
        Please use below identifier for time interval
        ---------------------------------------------
        D        calendar day frequency
        W        weekly frequency
        M        month end frequency
        Q        quarter end frequency
        A, Y     year end frequency
        H        hourly frequency
        T, min   minutely frequency
        ----------------------------------------------
        """
        ohlc = {
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
        } 
        try :
            data = data.resample(interval).apply(ohlc)
        except ValueError :
            sys.exit(print(offset))
            
        return data

    def _get_latest_data(self):
        """Check the latest data inserted to mongoDB
        Returns:
            epoch time : last excist data in mongoDB
        """
        client = self._mongo_connection()
        mycol = client[self._config['MONGO_DB']][self.symbol]
        latest_date = list(mycol.find({} , {"_id"}).sort("_id",-1).limit(1))

        return '1567965420000' if len(latest_date) == 0 else latest_date[0]["_id"]

    def _get_data(self):
        """check if data is already in mongoDB or not
            in case of not, collect data from binance api 
            and insert it to mongoDB
        """
        latest = date.fromtimestamp(int(self._get_latest_data()) / 1000)
        yesterday = date.today() - timedelta(days=1)

        if(latest != yesterday):
            self._collect_data(str(latest) , str(yesterday))
            self._insert_to_mongo()
