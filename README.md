# ftkafinance
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 
[![Python 3.6](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)


**[ftkfinance](https://github.com/hamednikseresht/ftkafinance.git)** is a finance Python package for collecting and analyzing market data using **`Binance Free API`**.

## Table of Contents
 - [Features](#features)
 - [Requirements](#requirements)
 - [Installation](#installation)
 - [Usage](#usage)
 - [License](#license)

## Features
 * Easy to setup and use.
 * No knowledge of Binance API and any credentials needed.
 * It is possible to collect any crypto candlestick data.
 * Also it is possible to work with this package with or without database. 

## Requirements
Install these following requirements in order to make sure the package will respond properly.
<br>

#### Softwares
- `Python interpreter`
- `Mongo DB database` (optional)

#### Packages 
1. `requests`
2. `pandas`
3. `python-dotenv`
4. `pymongo`
5. `ta-lib`

> ### Warning : it is essential to install [TA-LIB](http://mrjbq7.github.io/ta-lib/install.html) in your machine


## Installation
Currently you can install this package from github:

##### LINUX/MAC
```shell
pip install git+https://github.com/hamednikseresht/ftkafinance
```
##### WINDOWS
```shell
pip install git+https://github.com/hamednikseresht/ftkafinance #egg==httpie
```

## Usage
To use this package you have 2 option get data and strore it in a database or get data and use it without database. 

#### **load_crypto_data**
If you're project uses mongo db database and you want to store data you could use this method, as the following:

```python
from ftkafinance import Crypto

# invoke load_crypto_data method
Crypto.load_crypto_data(symbol='btcusdt', start_date='2020-01-01', end_date='2020-01-15', interval='1m')
```

#### **get_crypto_data**
If you want to retreive data and don't use database,you could use this second method, as the following:

```python
from ftkafinance import Crypto

# invoke get_crypto_data method
Crypto.get_crypto_data(symbol='btcusdt', start_date='2020-01-01', end_date='2020-01-15', interval='1m')
```

**Note:** Due to **`Binance API`** first date available to get data is `2019-10-01`
<br>

## License
This Package is licensed under [MIT](https://choosealicense.com/licenses/mit/) license

