from unittest.mock import sentinel
import pandas as pd
from eod_historical_data import (set_envar,
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
api_key = set_envar()
# api_key = "YOURAPI"


def test_get_eod_data_no_date():
    print(df := get_eod_data("AAPL", "US", api_key=api_key, session=session))
    # Note if df is Sentinel it means that the request was sent through but the response
    # was forbidden indicating that the APi Key may not have been authorized to perform the
    # Operation
    if df is not sentinel:
        assert df.index.name == "Date"


def test_get_eod_data_with_date():
    print(df := get_eod_data("AAPL", "US", start="2020-02-01", end="2020-02-10",
                      api_key=api_key, session=session))
    if df is not sentinel:
        assert df.index.name == "Date"
        assert df.index[0] != ""


def test_get_dividends():
    print(df := get_dividends("AAPL", "US", start="2020-02-01", end="2020-02-10",
                       api_key=api_key, session=session))
    if df is not sentinel:
        assert df.index.name == "Date"


def test_get_exchange_symbols():
    print(df := get_exchange_symbols(exchange_code="US",
                              api_key=api_key, session=session))
    if df is not sentinel:
        assert df.index.name == "Code"
        assert "AAPL" in df.index


def test_get_exchanges():
    print(df := get_exchanges())
    if df is not sentinel:
        assert df.index.name == "ID"
        assert "US" in df["Exchange Code"].unique()


def test_get_currencies():
    print(df := get_currencies())
    if df is not sentinel:
        assert df.index.name == "ID"
        assert "USD" in df["Currency Code"].unique()


def test_get_indexes():
    print(df := get_indexes())
    if df is not sentinel:
        assert df.index.name == "ID"
        assert "GSPC" in df["Code"].unique()
