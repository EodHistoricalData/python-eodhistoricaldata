import typing
import functools
import requests
import datetime
import traceback
import pandas as pd
from pandas.api.types import is_number
from urllib.parse import urlencode
from requests.exceptions import RetryError, ConnectTimeout
from config.config import Config

config_instance: Config = Config()
# NOTE do not remove
from unittest.mock import sentinel


def _init_session(session: typing.Union[requests.Session, None]) -> requests.Session:
    """
        Returns a requests.Session (or CachedSession)
    """
    return requests.Session() if session is None else session


def _url(url: str, params: dict) -> str:
    """
        Returns long url with parameters
        https://mydomain.com?param1=...&param2=...
    """
    return "{}?{}".format(url, urlencode(params)) if isinstance(params, dict) and len(params) > 0 else url


def _format_date(dt: typing.Union[None, datetime.datetime]) -> typing.Union[None, str]:
    """
        Returns formatted date
    """
    return None if dt is None else dt.strftime("%Y-%m-%d")


def _sanitize_dates(start: typing.Union[None, int], end: typing.Union[None, int]) -> tuple:
    """
        Return (datetime_start, datetime_end) tuple
    """
    if is_number(start):
        # regard int as year
        start: datetime.datetime = datetime.datetime(start, 1, 1)
    start = pd.to_datetime(start)

    if is_number(end):
        # regard int as year
        end: datetime.datetime = datetime.datetime(end, 1, 1)
    end = pd.to_datetime(end)

    if start and end:
        if start > end:
            raise Exception("end must be after start")

    return start, end


def _handle_request_errors(func: typing.Callable[..., typing.Union[pd.DataFrame, None]]) -> \
        typing.Union[None, typing.Callable[..., typing.Union[pd.DataFrame, None]]]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError:
            if config_instance.DEBUG is True:
                print(traceback.format_exc())
            else:
                print("Connection Error")
            return None
        except RetryError:
            if config_instance.DEBUG is True:
                print(traceback.format_exc())
            else:
                print("Connection Error")
            return None
        except ConnectTimeout:
            if config_instance.DEBUG is True:
                print(traceback.format_exc())
            else:
                print("Connection Error")
            return None

    return wrapper


def _handle_environ_error(func: typing.Callable[..., typing.Union[pd.DataFrame, None]]) -> \
        typing.Union[None, typing.Callable[..., typing.Union[pd.DataFrame, None]]]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            api_key: typing.Union[str, None] = kwargs.get('api_key')
            assert api_key is not None
            assert api_key != ""
            return func(*args, **kwargs)
        except AssertionError:
            raise EnvironNotSet("Environment not set see readme.md on how to setup your environment variables")

    return wrapper


# Errors

class RemoteDataError(IOError):
    """
    Remote data exception
    """
    pass


class EnvironNotSet(Exception):
    """
        raised when environment variables are not set
    """
    pass


api_key_not_authorized: int = 403
