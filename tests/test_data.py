import pandas as pd
from eod_historical_data import (get_api_key,
                                 get_eod_data,
                                 get_dividends,
                                 get_exchange_symbols,
                                 get_exchanges, get_currencies, get_indexes)
import datetime
import requests_cache

pd.set_option("max_rows", 10)

# Cache session (to avoid too much data consumption)
expire_after = datetime.timedelta(days=1)
session = requests_cache.CachedSession(cache_name='cache', backend='sqlite',
                                       expire_after=expire_after)

# Get API key
#  from environment variable
#  bash> export EOD_HISTORICAL_API_KEY="YOURAPI"
api_key = get_api_key()
# api_key = "YOURAPI"


def test_get_eod_data_no_date():
    df = get_eod_data("AAPL", "US", api_key=api_key, session=session)
    print(df)
    assert df.index.name == "Date"


def test_get_eod_data_with_date():
    df = get_eod_data("AAPL", "US", start="2016-02-01", end="2016-02-10",
                      api_key=api_key, session=session)
    print(df)
    assert df.index.name == "Date"
    assert df.index[0] == pd.to_datetime("2016-02-01")


def test_get_dividends():
    df = get_dividends("AAPL", "US", start="2016-02-01", end="2016-02-10",
                       api_key=api_key, session=session)
    print(df)
    assert df.index.name == "Date"


def test_get_exchange_symbols():
    df = get_exchange_symbols(exchange_code="US",
                              api_key=api_key, session=session)
    print(df)
    assert df.index.name == "Code"
    assert "AAPL" in df.index


def test_get_exchanges():
    df = get_exchanges()
    print(df)
    assert df.index.name == "ID"
    assert "US" in df["Exchange Code"].unique()


def test_get_currencies():
    df = get_currencies()
    print(df)
    assert df.index.name == "ID"
    assert "USD" in df["Currency Code"].unique()


def test_get_indexes():
    df = get_indexes()
    print(df)
    assert df.index.name == "ID"
    assert "GSPC" in df["Code"].unique()
