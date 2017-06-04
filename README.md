[![Build Status](https://travis-ci.org/femtotrader/python-eodhistoricaldata.svg?branch=master)](https://travis-ci.org/femtotrader/python-eodhistoricaldata)

# Python EOD Historical Data

A library to download data from EOD historical data https://eodhistoricaldata.com/ using:
- [Python](https://www.python.org/)
- [Requests](http://docs.python-requests.org/) / [Requests-cache](http://requests-cache.readthedocs.io/)
- [Pandas](http://pandas.pydata.org/)

## Installation

### Install latest development version

```bash
$ pip install git+https://github.com/femtotrader/python-eodhistoricaldata.git
```

or

```bash
$ git clone https://github.com/femtotrader/python-eodhistoricaldata.git
$ python setup.py install
```

## Usage

Environment variable `EOD_HISTORICAL_API_KEY` should be defined using:

```bash
export EOD_HISTORICAL_API_KEY="YOUR_API"
```

You can download data simply using

```python
In [1]: import pandas as pd
In [2]: pd.set_option("max_rows", 10)
In [3]: from eod_historical_data import get_eod_data
In [4]: df = get_eod_data("AAPL", "US")
In [5]: df
Out[1]:
                Open      High       Low     Close  Adjusted_close  \
Date
2000-01-03    3.7455    4.0179    3.6317    3.9978          3.9978
2000-01-04    3.8661    3.9509    3.6138    3.6607          3.6607
2000-01-05    3.7054    3.9487    3.6786    3.7143          3.7143
2000-01-06    3.7902    3.8214    3.3929    3.3929          3.3929
2000-01-07    3.4464    3.6071    3.4107    3.5536          3.5536
...              ...       ...       ...       ...             ...
2017-05-26  154.0000  154.2400  153.3100  153.6100        153.6100
2017-05-30  153.4200  154.4300  153.3300  153.6700        153.6700
2017-05-31  153.9700  154.1700  152.3800  152.7600        152.7600
2017-06-01  153.1700  153.3300  152.2200  153.1800        153.1800
2017-06-02  153.6000  155.4500  152.8900  155.4500        155.4500

                 Volume
Date
2000-01-03  133949200.0
2000-01-04  128094400.0
2000-01-05  194580400.0
2000-01-06  191993200.0
2000-01-07  115183600.0
...                 ...
2017-05-26   21927600.0
2017-05-30   20126900.0
2017-05-31   24451200.0
2017-06-01   16274200.0
2017-06-02   25163841.0

[4382 rows x 6 columns]
```

but if you want to avoid too much data consumption, you can use a cache mechanism.


```python
In [1]: import datetime        
In [2]: import requests_cache
In [3]: expire_after = datetime.timedelta(days=1)
In [4]: session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)
In [5]: df = get_eod_data("AAPL", "US", session=session)
```

See [tests directory](https://github.com/femtotrader/python-eodhistoricaldata/tree/master/tests) for example of other API endpoints.

## Credits

- Idea to create this project [came from this issue](https://github.com/pydata/pandas-datareader/issues/315) (Thanks [@deios0](https://github.com/deios0) )
- Code was inspired by [pandas-datareader](http://pandas-datareader.readthedocs.io/)
