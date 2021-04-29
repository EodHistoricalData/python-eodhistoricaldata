import typing

import requests
import datetime
import pandas as pd
from pandas.api.types import is_number
from urllib.parse import urlencode


def _init_session(session: requests.Session) -> requests.Session:
    """
        Returns a requests.Session (or CachedSession)
    """
    if session is None:
        return requests.Session()
    return session


def _url(url: str, params: dict) -> str:
    """
        Returns long url with parameters
        https://mydomain.com?param1=...&param2=...
    """
    if params is not None and len(params) > 0:
        return url + "?" + urlencode(params)
    else:
        return url


class RemoteDataError(IOError):
    """
    Remote data exception
    """
    pass


def _format_date(dt: typing.Union[None, datetime.datetime]) -> typing.Union[None, str]:
    """
    Returns formated date
    """
    if dt is None:
        return dt
    return dt.strftime("%Y-%m-%d")


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

    if start is not None and end is not None:
        if start > end:
            raise Exception("end must be after start")

    return start, end
