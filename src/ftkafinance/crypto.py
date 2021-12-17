import sys
import requests
import pandas as pd
from datetime import datetime, timedelta, date
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

    @classmethod
    def set_symbol(cls, symbol: str):
        """ set the symbol of the class
        Parameters
        ----------
        symbol : str
            symbol supported by Binance API.
        """
        cls._symbol = symbol

    @classmethod
    def _progress(cls, count, total, status=''):
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

    @classmethod
    def _str_to_epoch_ms(cls, date: str):
        """ convert date string to epoch time in miliseconds """
        str_data = str(date)
        return int(datetime.strptime(str_data, '%Y-%m-%d').timestamp()*1000)

    @classmethod
    def _get_latest_data(cls):
        """Check the latest data inserted to mongoDB
        Returns:
            epoch time : last excist data in mongoDB
        """
        client = cls._mongo_connection()
        mycol = client[cls._config['MONGO_DB']][cls._symbol]
        latest_date = list(mycol.find({}, {"_id"}).sort("_id", -1).limit(1))

        return '1567965420000' if len(latest_date) == 0 else latest_date[0]["_id"]

    @classmethod
    def _symbols_list(cls):
        """ return a list of binance valid symbols
        """
        try:
            resp = requests.get(
                url='https://fapi.binance.com/fapi/v1/exchangeInfo', timeout=10)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            raise SystemExit("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            raise SystemExit("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            raise SystemExit("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            raise SystemExit("OOps: Something Else", err)

        data = resp.json()

        # create a list of valid symbols
        symbol_list = [s['symbol'].lower() for s in data['symbols']]

        return symbol_list

    @classmethod
    def _mongo_connection(cls):
        """ connect to mongoDB with credentials from .env file
        Returns:
            Mongo Client Oject
        """
        client = MongoClient(
            cls._config['MONGO_Host'],
            int(cls._config['MONGO_Port']),
            username=cls._config['MONGO_User'],
            password=cls._config['MONGO_Password'])
        return client

    @classmethod
    def _insert_to_mongo(cls):
        """ insert data to mongoDB
            read .env file to get mongoDB credentials
            create a new collection if it doesn't exist
        """
        client = cls._mongo_connection()
        try:
            client
        except Exception as exp:
            raise SystemExit(exp)

        mycol = client[cls._config['MONGO_DB']][cls._symbol]
        # Set the unique index using the open time
        cls._df['_id'] = cls._df.OpenTime.astype(str)
        # First convert the dataframe to a list of dictionaries
        # then insert the list into the collection with json format
        try:
            # Ignore duplicate records
            json_list = json.loads(json.dumps(list(cls._df.T.to_dict().values())))
            mycol.insert_many(json_list, ordered=False)
        except Exception:
            pass

    @classmethod
    def _tf_maker(cls, data, interval):
        """ transform data to desire time frequency
            with candle stick and volume data pattern
        """
        offset = """
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
                'Volume': 'sum'}
        try:
            data = data.resample(interval).apply(ohlc)
        except ValueError:
            sys.exit(print(offset))

        return data

    @classmethod
    def _clean_data(cls, data):
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
        data['Open'] = pd.to_numeric(data['Open'], downcast="float")
        data['High'] = pd.to_numeric(data['High'], downcast="float")
        data['Low'] = pd.to_numeric(data['Low'], downcast="float")
        data['Close'] = pd.to_numeric(data['Close'], downcast="float")
        data['Volume'] = pd.to_numeric(data['Volume'], downcast="float")

        return data[['Open', 'High', 'Low', 'Close', 'Volume']]

    @classmethod
    def _data_update(cls, data_frame):
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
        data_frame = data_frame.append(cls._data_to_df(start.isoformat(),
                                                       end.isoformat()))
        return data_frame

    @classmethod
    def _data_to_df(cls, start_time: str, end_time: str):
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
        start = cls._str_to_epoch_ms(start_time)
        end = cls._str_to_epoch_ms(end_time)

        if end < start:
            raise SystemExit("End date must be larger than start date")

        url = 'https://fapi.binance.com/fapi/v1/klines'
        params = {
                    'symbol': str(cls._symbol),
                    'interval': '1m',
                    'startTime': start,
                    'endTime': end,
                    'limit': '1500'}
        try:
            request = requests.get(url, params=params)
        except requests.exceptions.RequestException as exp:
            raise SystemExit(exp)

        data = request.json()
        if type(data) == dict:
            raise SystemExit(f"error code: {data['code']}\nmessage : \
                {data['msg']}")
        try:
            data[0]
        except IndexError:
            raise SystemExit("there is no response from your request")

        if len(data) == 1500:
            print("Warning :\nthe limit rate for binance API is 1500 ")
        df = pd.DataFrame(data)
        df.columns = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume',
                      'CloseTime', 'QuoteVolume', 'TradesNumber',
                      'TakerBaseVolume', 'TakerQuoteVolume', 'Ignore']
        df.index = df.OpenTime

        return df

    @classmethod
    def _collect_data(cls, start_date: str, end_date: str):
        """ Split request with large interval time to smaller request in
        order to over come binance api limitaion
        Parameters
        ----------
        start_time : str
            start date for retrieving data  format: 2020-12-30.
        end_time : str
            end date for retrieving data: 2020-12-30.
        """
        date_range = pd.date_range(start_date, end_date)
        for i, day in enumerate(date_range):
            if len(date_range) > i+1:
                cls._df = cls._df.append(
                        cls._data_to_df(day.strftime('%Y-%m-%d'),
                                        date_range[i+1].strftime('%Y-%m-%d')))
                cls._progress(i, len(date_range),
                              status=f"{cls._symbol} data is loading")
            if i % 50 == 0:
                time.sleep(2)

    @classmethod
    def _get_data(cls):
        """check if data is already in mongoDB or not
            in case of not, collect data from binance api
            until the end of yesterday and insert it to mongoDB
        """
        # check latest data in mongoDB
        # -100 is for avoiding confussion in time 00:00:00
        latest = date.fromtimestamp((int(cls._get_latest_data()) / 1000)-100)
        yesterday = date.today() - timedelta(days=1)
        if(latest != yesterday):
            cls._collect_data(str(latest), str(date.today()))
            cls._insert_to_mongo()

    @staticmethod
    def load_crypto_data(symbol, start_date='2019-01-01',
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
        # check if input symbol is valid
        if symbol.lower() not in Crypto._symbols_list():
            raise SystemExit("Symbol is not valid \n\
                Please select correct symbol: \n{}".format(Crypto._symbols_list()))

        Crypto.set_symbol(symbol)
        client = Crypto._mongo_connection()
        mycol = client[Crypto._config['MONGO_DB']][Crypto._symbol]
        try:
            mycol
        except Exception as exp:
            raise SystemExit(exp)

        start = Crypto._str_to_epoch_ms(start_date)
        end = Crypto._str_to_epoch_ms(end_date)
        today = Crypto._str_to_epoch_ms(str(date.today()))
        latest = int(Crypto._get_latest_data())

        # check data exist in database
        if end > latest:
            Crypto._get_data()

        # get interval data from mongoDB and convert it to a pandas data frame
        data = pd.DataFrame(list(mycol.find(
            {'_id': {'$gt': str(start),
                     '$lt': str(end)}})))

        # today data , append to database fetched data
        if (end >= today and start <= today):
            data = Crypto._data_update(data)

        if data.empty:
            raise SystemExit("There is no valid data for this interval")

        data = Crypto._clean_data(data)

        return Crypto._tf_maker(data, interval)
