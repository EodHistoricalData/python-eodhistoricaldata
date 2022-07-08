from sqlite3 import Timestamp
from typing import Optional, Union, Dict, Tuple, Callable
import functools
import requests
from datetime import date, datetime
import traceback
import pandas as pd
import pandas.api.types as _types
from urllib.parse import urlencode
from requests.exceptions import RetryError, ConnectTimeout
from config.config import Config

config_instance: Config = Config()
# NOTE do not remove


Sanitize_Type = Tuple[Union[Timestamp, datetime], Union[Timestamp, datetime]]
Handle_Request_Type = Callable[..., Optional[pd.DataFrame]]


def _init_session(session: Optional[requests.Session]) -> requests.Session:
    """
        Returns a requests.Session (or CachedSession)
    """
    return requests.Session() if session is None else session


def _url(url: str, params: Dict[str, str]) -> str:
    """
        Returns long url with parameters
        https://mydomain.com?param1=...&param2=...
    """
    return "{}?{}".format(url, urlencode(params)) if isinstance(params, dict) and len(params) > 0 else url


def _format_date(dt: Optional[datetime]) -> Optional[str]:
    """
        Returns formatted date
    """
    return None if dt is None else dt.strftime("%Y-%m-%d")


def _sanitize_dates(start: Union[int, date, datetime], end: Union[int, date, datetime]) -> Sanitize_Type:
    """
        Return (datetime_start, datetime_end) tuple
    """
    if start and end:
        if start > end:
            raise ValueError("end must be after start")
    else:
        raise ValueError("start and or end must contain valid int. date or datetime object")

    start = datetime(start, 1, 1) if _types.is_number(start) else pd.to_datetime(start)
    end = datetime(end, 1, 1) if _types.is_number(end) else pd.to_datetime(end)

    return start, end


def _handle_request_errors(func: Handle_Request_Type) -> Optional[Handle_Request_Type]:
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


def _handle_environ_error(func: Handle_Request_Type) -> Optional[Handle_Request_Type]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            api_key: Optional[str] = kwargs.get('api_key')
            assert api_key is not None
            assert api_key != ""
            return func(*args, **kwargs)
        except AssertionError:
            raise EnvironNotSet("Environment not set, see readme.md on how to setup your environment variables")

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
