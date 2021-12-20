from datetime import date
from numpy.lib.stride_tricks import DummyArray
from pymongo import MongoClient
from numpy import empty
import pandas as pd
import sys

sys.path.insert(1, './src/ftkafinance')
from crypto import Crypto

class Test:


    _data = pd.DataFrame()

    def __init__(self) -> None:
        self.test_set_symbol()
        self.test_str_to_epoch_ms()
        self.test_get_latest_data()
        self.test_symbol_list()
        self.test_check_interval()
        self.test_mongo_connection()
        self.test_insert_to_mongo()
        self.test_clean_data()
        self.test_tf_maker() 
        self.test_data_update()
        self.test_data_to_df()
        self.test_collect_data()
        self.test_load_crypto_data()
        self.test_get_crypto_data()

    @classmethod
    def _creat_dummy_data(cls):
        dummy = [
            {
                "_id": "1639773000000",
                "OpenTime": 1639773000000,
                "Open": "46388.20",
                "High": "46408.00",
                "Low": "46325.12",
                "Close": "46374.75",
                "Volume": "219.224",
                "CloseTime": "1639773059999",
                "QuoteVolume": "10163168.48423",
                "TradesNumber": 3031,
                "TakerBaseVolume": "81.102",
                "TakerQuoteVolume": "3760618.01027",
            },
            {
                "_id": "1639772940000",
                "OpenTime": 1639772940000,
                "Open": "46377.62",
                "High": "46417.95",
                "Low": "46342.10",
                "Close": "46388.19",
                "Volume": "328.169",
                "CloseTime": "1639772999999",
                "QuoteVolume": "15220411.95135",
                "TradesNumber": 3857,
                "TakerBaseVolume": "202.211",
                "TakerQuoteVolume": "9378607.20504",
            },
            {
                "_id": "1639772880000",
                "OpenTime": 1639772880000,
                "Open": "46364.65",
                "High": "46390.37",
                "Low": "46224.46",
                "Close": "46377.62",
                "Volume": "1067.931",
                "CloseTime": "1639772939999",
                "QuoteVolume": "49446312.20559",
                "TradesNumber": 10080,
                "TakerBaseVolume": "412.758",
                "TakerQuoteVolume": "19116990.00530"
            },
            {
                "_id": "1639772820000",
                "OpenTime": 1639772820000,
                "Open": "46488.00",
                "High": "46491.79",
                "Low": "46324.19",
                "Close": "46364.65",
                "Volume": "936.997",
                "CloseTime": "1639772879999",
                "QuoteVolume": "43477610.18947",
                "TradesNumber": 7620,
                "TakerBaseVolume": "174.295",
                "TakerQuoteVolume": "8087850.76098"
            }
        ]
        test_df = pd.DataFrame()
        for item in dummy:
            test_df = test_df.append(item, ignore_index=True)
        test_df.index = test_df._id
        test_df = test_df.iloc[: , :-1]

        return test_df

    @staticmethod
    def test_set_symbol():
        Crypto.set_symbol('ethusdt')
        if Crypto._symbol is not empty:
            print('pass: _symbol_list')
        else:
            assert False, 'symbol is not set'

    @staticmethod
    def test_str_to_epoch_ms():
        var = Crypto._str_to_epoch_ms(str(date.today()))
        if isinstance(var, int) and len(str(var)) == 13:
            print('pass: _str_to_epoch_ms')
        else:
            assert False, 'varible is not integer or\
                           number is not in milisecond format'

    @staticmethod
    def test_get_latest_data():
        Crypto.set_symbol('btcusdt')
        var = Crypto._get_latest_data()
        
        if len(var) != 0:
            print('pass: _get_latest_data')
        else:
            assert False, 'latest data is not valid'

    @staticmethod
    def test_symbol_list():
        if len(Crypto._symbols_list()) != 0:
            print('pass: _symbol_list')
        else:
            assert False, 'list is not valid'

    @staticmethod
    def test_check_interval():
        if len(Crypto._check_interval()['intervals']) != 0:
            print('pass: _check_interval')
        else:
            assert False, 'list is not valid'

    @staticmethod
    def test_mongo_connection():
        var = Crypto._mongo_connection()
        if isinstance(var, MongoClient):
            print('pass: _mongo_connection')
        else:
            assert False, 'can not establish connection to mongo'
        # return len(var)

    @staticmethod
    def test_insert_to_mongo():
        backup = Crypto._df
        dummy = {
            'OpenTime': -1,
            'Open': '-1',
            'data': 'test db insert method'
        }
        
        # set symbol
        Crypto.set_symbol('btcusdt')
        # append test data to df
        Crypto._df = Crypto._df.append(dummy, ignore_index=True)
        # call insert to mongo object
        Crypto._insert_to_mongo()

        # connect to db
        client = Crypto._mongo_connection()
        # select table
        mycol = client[Crypto._config['MONGO_DB']][Crypto._symbol]
        # check if dummy data iserted to db
        if len(list(mycol.find({'_id':'-1.0'}))) > 0:
            # delete dummy data from db
            mycol.delete_one({'_id':'-1.0'})
            Crypto._df = backup
            print('pass: _insert_to_mongo')
        else:
            assert False, 'could not connect to database and insert data'

    @staticmethod
    def test_clean_data():
        test_df = Test._creat_dummy_data()
        
        test = Crypto._clean_data(test_df)

        if len(test) > 0:
            Test._data = Test._data.append(test)
            print('pass: _clean_data')
        else:
            assert False, 'data cleaning error'

    @staticmethod
    def test_tf_maker():
        Test.test_clean_data()

        test = Crypto._tf_maker(Test._data , '1d')
        
        if len(test) > 0:
            Test._data = Test._data.append(test)
            print('pass: _tf_maker')
        else:
            assert False, '_tf_maker error'

    @staticmethod
    def test_data_update():
        Crypto.set_symbol('ethusdt')
        test_data = pd.DataFrame()
        test = Crypto._data_update(test_data)

        if len(test) > 0:
            print('pass: _data_update')
        else:
            assert False, '_data_update error'

    @staticmethod
    def test_data_to_df():
        date_collection = [
                          {'start': '2020-01-01', 'end': '2020-01-03', 'interval': '1m'},
                          {'start': '2020-05-01', 'end': '2020-05-05', 'interval': '30m'},
                          {'start': '2020-01-01', 'end': '2020-01-05', 'interval': '6h'},
                          {'start': '2021-10-01', 'end': '2021-10-05', 'interval': '1d'}
                          ]
        Crypto.set_symbol('btcusdt')
        result = []
        for item in date_collection:
            result.append(Crypto._data_to_df(item['start'], item['end'], item['interval']))

        if len(result) == 4:
            print('pass: _data_to_df')
        else:
            assert False, '_data_to_df error'            

    @staticmethod
    def test_collect_data():
        date_collection = {'start': '2020-01-01', 
                           'end': '2020-01-03', 
                           'interval': '1m'}

        Crypto.set_symbol('btcusdt')
        Crypto._collect_data(date_collection['start'],
                             date_collection['end'], 
                             date_collection['interval'])

        if len(Crypto._df) == 0:
            assert False, '_collect_data error'         
        else:
            print('pass: _collect_data \n'+'pass: _get_data')

    @staticmethod
    def test_load_crypto_data():
        date_collection = {'symbol': 'btcusdt',
                           'start': '2020-01-01',
                           'end': '2020-01-10',
                           'interval': '1T'}
  
        result = Crypto.load_crypto_data(date_collection['symbol'],
                                         date_collection['start'],
                                         date_collection['end'],
                                         date_collection['interval'])
        
        if len(result) == 0:
            assert False, 'load_crypto_data error'         
        else:
            print('pass: load_crypto_data')

    @staticmethod
    def test_get_crypto_data():
        date_collection = {'symbol': 'btcusdt',
                           'start': '2020-01-01',
                           'end': '2020-01-10',
                           'interval': '1h'}
  
        result = Crypto.get_crypto_data(date_collection['symbol'],
                                         date_collection['start'],
                                         date_collection['end'],
                                         date_collection['interval'])
        
        if len(result) == 0:
            assert False, 'get_crypto_data error'         
        else:
            print('pass: get_crypto_data')

