import typing
import aiohttp as aiohttp
import requests
import pandas as pd
from io import StringIO
from ._utils import (_init_session, _format_date,
                     _sanitize_dates, _url, RemoteDataError, _handle_request_errors, EnvironNotSet,
                     _handle_environ_error, sentinel, api_key_not_authorized)

from config.config import Config

config_data: Config = Config()

EOD_HISTORICAL_DATA_API_KEY_ENV_VAR: str = config_data.EOD_HISTORICAL_DATA_API_KEY_ENV_VAR
EOD_HISTORICAL_DATA_API_KEY_DEFAULT: str = config_data.EOD_HISTORICAL_DATA_API_KEY_DEFAULT
EOD_HISTORICAL_DATA_API_URL: str = config_data.EOD_HISTORICAL_DATA_API_URL


def set_envar() -> str:
    return EOD_HISTORICAL_DATA_API_KEY_ENV_VAR


@_handle_environ_error
@_handle_request_errors
def get_eod_data(symbol: str, exchange: str, start: typing.Union[str, int] = None, end: typing.Union[str, int] = None,
                 api_key: str = EOD_HISTORICAL_DATA_API_KEY_DEFAULT,
                 session: typing.Union[None, requests.Session] = None) -> typing.Union[pd.DataFrame, None]:
    """
        Returns EOD (end of day data) for a given symbol
    """
    symbol_exchange: str = "{}.{}".format(symbol, exchange)
    session: requests.Session = _init_session(session)
    start, end = _sanitize_dates(start, end)
    endpoint: str = "/eod/{}".format(symbol_exchange)
    url: str = EOD_HISTORICAL_DATA_API_URL + endpoint
    params: dict = {
        "api_token": api_key,
        "from": _format_date(start),
        "to": _format_date(end)
    }
    r: requests.Response = session.get(url, params=params)
    print('status code : {}'.format(r.status_code))

    if r.status_code == requests.codes.ok:
        # NOTE engine='c' which is default does not support skip footer
        df: typing.Union[pd.DataFrame, None] = pd.read_csv(StringIO(r.text), engine='python',
                                                           skipfooter=1, parse_dates=[0], index_col=0)
        return df
    elif r.status_code == api_key_not_authorized:
        print("API Key Restricted, Try upgrading your API Key: {}".format(__name__))
        return sentinel
    else:
        params["api_token"] = "YOUR_HIDDEN_API"
        raise RemoteDataError(r.status_code, r.reason, _url(url, params))


@_handle_environ_error
@_handle_request_errors
async def get_eod_data_async(symbol: str, exchange: str, start: typing.Union[str, int] = None,
                             end: typing.Union[str, int] = None,
                             api_key: str = EOD_HISTORICAL_DATA_API_KEY_DEFAULT) -> typing.Union[pd.DataFrame, None]:
    symbol_exchange: str = "{}.{}".format(symbol, exchange)
    start, end = _sanitize_dates(start, end)
    endpoint: str = "/eod/{}".format(symbol_exchange)
    url: str = EOD_HISTORICAL_DATA_API_URL + endpoint
    params: dict = {
        "api_token": api_key,
        "from": _format_date(start),
        "to": _format_date(end)
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                response_data = await response.text()
                df: typing.Union[pd.DataFrame, None] = pd.read_csv(StringIO(response_data), engine='python',
                                                                   skipfooter=1, parse_dates=[0], index_col=0)
                return df
            elif response.status == api_key_not_authorized:
                print("API Key Restricted, Try upgrading your API Key: {}".format(__name__))
                return sentinel
            else:
                params["api_token"] = "YOUR_HIDDEN_API"
                raise RemoteDataError(response.status, response.reason, _url(url, params))


@_handle_environ_error
@_handle_request_errors
def get_dividends(symbol: str, exchange: str, start: typing.Union[str, int] = None, end: typing.Union[str, int] = None,
                  api_key: str = EOD_HISTORICAL_DATA_API_KEY_DEFAULT,
                  session: typing.Union[None, requests.Session] = None) -> typing.Union[pd.DataFrame, None]:
    """
        Returns dividends
    """
    symbol_exchange: str = "{},{}".format(symbol, exchange)
    session: requests.Session = _init_session(session)
    start, end = _sanitize_dates(start, end)
    endpoint: str = "/div/{}".format(symbol_exchange)
    url: str = EOD_HISTORICAL_DATA_API_URL + endpoint
    params: dict = {
        "api_token": api_key,
        "from": _format_date(start),
        "to": _format_date(end)
    }
    r: requests.Response = session.get(url, params=params)
    print('status code : {}'.format(r.status_code))

    if r.status_code == requests.codes.ok:
        # NOTE engine='c' which is default does not support skip footer
        df: typing.Union[None, pd.DataFrame] = pd.read_csv(StringIO(r.text), engine='python', skipfooter=1,
                                                           parse_dates=[0], index_col=0)
        assert len(df.columns) == 1
        ts = df["Dividends"]
        return ts
    elif r.status_code == api_key_not_authorized:
        print("API Key Restricted, Try upgrading your API Key: {}".format(__name__))
        return sentinel
    else:
        params["api_token"] = "YOUR_HIDDEN_API"
        raise RemoteDataError(r.status_code, r.reason, _url(url, params))


@_handle_environ_error
@_handle_request_errors
async def get_dividends_async(symbol: str, exchange: str, start: typing.Union[str, int] = None,
                              end: typing.Union[str, int] = None,
                              api_key: str = EOD_HISTORICAL_DATA_API_KEY_DEFAULT) -> typing.Union[pd.DataFrame, None]:
    """
        Returns dividends
    """
    symbol_exchange: str = "{},{}".format(symbol, exchange)
    start, end = _sanitize_dates(start, end)
    endpoint: str = "/div/{}".format(symbol_exchange)
    url: str = EOD_HISTORICAL_DATA_API_URL + endpoint
    params: dict = {
        "api_token": api_key,
        "from": _format_date(start),
        "to": _format_date(end)
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                response_data = await response.text()
                df: typing.Union[None, pd.DataFrame] = pd.read_csv(StringIO(response_data), engine='python',
                                                                   skipfooter=1,
                                                                   parse_dates=[0], index_col=0)
                assert len(df.columns) == 1
                ts = df["Dividends"]
                return ts
            elif response.status == api_key_not_authorized:
                print("API Key Restricted, Try upgrading your API Key: {}".format(__name__))
                return sentinel
            else:
                params["api_token"] = "YOUR_HIDDEN_API"
                raise RemoteDataError(response.status, response.reason, _url(url, params))


@_handle_environ_error
@_handle_request_errors
def get_exchange_symbols(exchange_code: str,
                         api_key: str = EOD_HISTORICAL_DATA_API_KEY_DEFAULT,
                         session: typing.Union[requests.Session, None] = None) -> typing.Union[pd.DataFrame, None]:
    """
    Returns list of symbols for a given exchange
    """
    session: requests.Session = _init_session(session)
    endpoint: str = "/exchanges/{exchange_code}".format(exchange_code=exchange_code)
    url: str = EOD_HISTORICAL_DATA_API_URL + endpoint
    params: dict = {
        "api_token": api_key
    }
    r: requests.Response = session.get(url, params=params)
    print('status code : {}'.format(r.status_code))
    if r.status_code == requests.codes.ok:
        df: typing.Union[None, pd.DataFrame] = pd.read_csv(StringIO(r.text), engine='python', skipfooter=1, index_col=0)
        return df
    elif r.status_code == api_key_not_authorized:
        print("API Key Restricted, Try upgrading your API Key: {}".format(__name__))
        return sentinel
    else:
        params["api_token"] = "YOUR_HIDDEN_API"
        raise RemoteDataError(r.status_code, r.reason, _url(url, params))


@_handle_environ_error
@_handle_request_errors
async def get_exchange_symbols_async(exchange_code: str,
                                     api_key: str = EOD_HISTORICAL_DATA_API_KEY_DEFAULT) -> \
        typing.Union[pd.DataFrame, None]:

    """
        Returns list of symbols for a given exchange
    """
    endpoint: str = "/exchanges/{exchange_code}".format(exchange_code=exchange_code)
    url: str = EOD_HISTORICAL_DATA_API_URL + endpoint
    params: dict = {
        "api_token": api_key
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                response_data = await response.text()
                df: typing.Union[None, pd.DataFrame] = pd.read_csv(StringIO(response_data), engine='python',
                                                                   skipfooter=1, index_col=0)
                return df
            elif response.status == api_key_not_authorized:
                print("API Key Restricted, Try upgrading your API Key: {}".format(__name__))
                return sentinel
            else:
                params["api_token"] = "YOUR_HIDDEN_API"
                raise RemoteDataError(response.status, response.reason, _url(url, params))


def get_exchanges() -> pd.DataFrame:
    """
    Returns list of exchanges
    https://eodhistoricaldata.com/knowledgebase/list-supported-exchanges/
    """
    data: str = """ID	Exchange Name	Exchange Code
1	Munich Exchange	MU
2	Berlin Exchange	BE
3	Frankfurt Exchange	F
4	Stuttgart Exchange	STU
5	Mexican Exchange	MX
6	Hanover Exchange	HA
8	Australian Exchange	AU
9	Singapore Exchange	SG
10	Indexes	INDX
11	USA Stocks	US
12	Kuala Lumpur Exchange	KLSE
13	Funds	FUND
14	Bombay Exchange	BSE
15	Dusseldorf Exchange	DU
16	London Exchange	LSE
17	Euronext Paris	PA
18	XETRA Exchange	XETRA
19	NSE (India)	NSE
20	Hong Kong Exchange	HK
21	Borsa Italiana	MI
22	SIX Swiss Exchange	SW
23	Hamburg Exchange	HM
24	Toronto Exchange	TO
25	Stockholm Exchange	ST
26	Oslo Stock Exchange	OL
27	Euronext Amsterdam	AS
28	Coppenhagen Exchange	CO
29	Euronext Lisbon	LS
30	Korea Stock Exchange	KO
31	Shanghai Exchange	SS
32	Taiwan Exchange	TW
33	Sao Paolo Exchange	SA
34	Euronext Brussels	BR
35	Madrid Exchange	MC
36	Vienna Exchange	VI
37	New Zealand Exchange	NZ
38	FOREX	FX
39	London IL	IL
40	Irish Exchange	IR
41	MICEX Russia	MCX
42	OTC Market	OTC
43	ETF-Euronext	NX
44	Johannesburg Exchange	JSE"""
    df: typing.Union[pd.DataFrame, None] = pd.read_csv(StringIO(data), sep="\t")
    df: pd.DataFrame = df.set_index("ID")
    return df


def get_currencies() -> pd.DataFrame:
    """
    Returns list of supported currencies
    https://eodhistoricaldata.com/knowledgebase/list-supported-currencies/
    """
    data: str = """ID	Exchange Code	Currency Code
1	FX	USD
2	FX	EUR
3	FX	RUB
4	FX	GBP
5	FX	CNY
6	FX	JPY
7	FX	SGD
8	FX	INR
9	FX	CHF
10	FX	AUD
11	FX	CAD
12	FX	HKD
13	FX	MYR
14	FX	NOK
15	FX	NZD
16	FX	ZAR
17	FX	SEK
18	FX	DKK
19	FX	BRL
20	FX	ZAC
21	FX	MXN
22	FX	TWD
23	FX	KRW
24	FX	CLP
25	FX	CZK
26	FX	HUF
27	FX	IDR
28	FX	ISK
29	FX	MXV
30	FX	PLN
31	FX	TRY
32	FX	UYU
33	FX	BTC"""
    df: typing.Union[pd.DataFrame, None] = pd.read_csv(StringIO(data), sep="\t")
    df: pd.DataFrame = df.set_index("ID")
    return df


def get_indexes() -> pd.DataFrame:
    """
    Returns list of supported indexes
    https://eodhistoricaldata.com/knowledgebase/list-supported-indexes/
    """
    data: str = """ID	Exchange Code	Code	Index Name
1	INDX	GSPC	S&P 500
2	INDX	GDAXI	DAX Index
3	INDX	SSEC	Shanghai Composite Index (China)
4	INDX	MERV	MERVAL Index (Argentina)
5	INDX	FTSE	FTSE 100 Index (UK)
6	INDX	AORD	All Ordinaries Index (Australia)
7	INDX	BSESN	BSE 30 Sensitivity Index (SENSEX)
8	INDX	VIX	VIX S&P 500 Volatility Index
9	INDX	HSI	Hang Seng Index (Hong Kong)
10	INDX	GSPTSE	S&P TSX Composite Index (Canada)
11	INDX	FCHI	CAC 40 Index
12	INDX	TA100	Tel Aviv 100 Index (Israel
13	INDX	CYC	Morgan Stanley Cyclical Index
14	INDX	IIX	Interactive Week Internet Index
15	INDX	CMR	Morgan Stanley Consumer Index
16	INDX	GOX	CBOE Gold Inde
17	INDX	RTS_RS	RTSI Index
18	INDX	GD_AT	Athens Composite Inde
19	INDX	FTSEMIB_MI	Untitled Dataset 2015-07-13 20:00:12
20	INDX	WILREIT	Wilshire US REIT Inde
21	INDX	W5KMCG	Wilshire US Mid Cap Growt
22	INDX	IBEX	IBEX 35 Index
23	INDX	W5KLCV	Wilshire US Large Cap Valu
24	INDX	SSMI	Swiss Market Index
25	INDX	OEX	S&P 100 Inde
26	INDX	RUI	Russell 1000 Inde
27	INDX	XAX	NYSE AMEX Composite Inde
28	INDX	WILRESI	Wilshire US Real Estate Securities Inde
29	INDX	NZ50	NZSE 50 (New Zealand)
30	INDX	UTY	PHLX Utility Sector Inde
31	INDX	CSE	Colombo All Shares Index (Sri Lanka
32	INDX	XOI	NYSE AMEX Oil Inde
33	INDX	OSX	PHLX Oil Service Sector Inde
34	INDX	XAL	NYSE AMEX Airline Inde
35	INDX	W5KSCG	Wilshire US Small Cap Growt
36	INDX	TWII	Taiwan Weighted Inde
37	INDX	ATX	ATX Index (Austria
38	INDX	NWX	NYSE ARCA Networking Inde
39	INDX	W5KSCV	Wilshire US Small Cap Valu
40	INDX	XAU	PHLX Gold/Silver Sector Inde
41	INDX	W5KMCV	Wilshire US Mid Cap Valu
42	INDX	WGREIT	Wilshire Global REIT Inde
43	INDX	SML	S&P Small-Cap 600 Inde
44	INDX	RUT	Russell 2000 Inde
45	INDX	JKSE	Jakarta Composite Index (Indonesia
46	INDX	BFX	Euronext BEL-20 Index (Belgium)
47	INDX	XBD	NYSE AMEX Securities Broker/Dealer Inde
48	INDX	RUA	Russell 3000 Inde
49	INDX	XII	NYSE ARCA Institutional Inde
50	INDX	IETP	ISEQ 20 Price Index (Ireland
51	INDX	DRG	NYSE AMEX Pharmaceutical Inde
52	INDX	W5000	Wilshire 5000 Total Market Inde
53	INDX	HGX	PHLX Housing Sector Inde
54	INDX	MXX	IPC Index (Mexico)
55	INDX	W5KLCG	Wilshire US Large Cap Growt
56	INDX	STI	Straits Times Index
57	INDX	KS11	KOSPI Composite Index
58	INDX	AEX	AEX Amsterdam Index
59	INDX	NYA	NYSE Composite Index
60	INDX	XMI	NYSE ARCA Major Market Inde
61	INDX	BTK	NYSE AMEX Biotechnology Inde
62	INDX	EPX	NASDAQ SIG Oil Exploration and Production Inde
63	INDX	MID	S&P Mid-Cap 400 Inde
64	INDX	HUI	NYSE Arca Gold Bugs Inde
65	INDX	SOX	PHLX Semiconductor Inde
66	INDX	HCX	CBOE S&P Healthcare Index
67	INDX	XCI	NYSE AMEX Computer Technology Inde
68	INDX	XNG	NYSE AMEX Natural Gas Inde
69	INDX	RMZ	MSCI US REIT Inde
70	INDX	WGRESI	Wilshire Global Real Estate Securities Inde
71	INDX	N225	Nikkei 225 Index (Japan
72	INDX	VDAX	Deutsche Boerse VDAX Volatility Inde
73	INDX	MXY	NYSE ARCA Mexico Inde
74	INDX	OSEAX	Oslo Exchange All Share Index (Norway)
75	INDX	TYX	Treasury Yield 30 Years Inde
76	INDX	DJI	Dow Jones Industrial Average
77	INDX	AXPJ	S&P/ASX 200 Australia REIT Inde
78	INDX	PSI20	PSI 20 Stock Index (Portugal
79	INDX	IRX	13-week Treasury Bill Inde
80	INDX	FVX	Treasury Yield 5 Years Inde
81	INDX	NYI	NYSE International 100 Index
82	INDX	AXJO	S&P/ASX 200 Index (Australia
83	INDX	512NTR	S&P 500 GBP Hdg (Net TR) (^512NTR)
84	INDX	CTES_VI	Czech Trading Inde
85	INDX	NSEI	S&P/CNX Nifty Index (India
86	INDX	NYY	NYSE TMT Inde
87	INDX	CCSI	EGX 70 Price Index (Egypt
88	INDX	SPSUPX	S&P Composite 1500 Inde
89	INDX	BVSP	Bovespa Index (Brazil)
90	INDX	ISEQ	ISEQ Overall Price Index (Ireland
91	INDX	JPN	NYSE AMEX Japan Inde
92	INDX	NYL	NYSE World Leaders Inde
93	INDX	TNX	CBOE Interest Rate 10-Year T-Note Inde
94	INDX	NY	NYSE US 100 Inde
95	INDX	SPLV	PowerShares S&P 500 Low Volatil
96	INDX	OMXSPI	Stockholm General Index (Sweden)
97	INDX	GVZ	CBOE Gold Volatility Inde
98	INDX	SPY	SPDR S&P 500 (SPY
99	INDX	IEQR_IR	ISEQ General Total Return Index (Ireland
100	INDX	OMXC20_CO	OMX Copenhagen 20 Index
101	INDX	DJUSFN	^DJUSFN: Dow Jones U.S. Financials Inde
102	INDX	DJASD	^DJASD: Dow Jones Asia Select Dividen
103	INDX	IMUS	^IMUS: Dow Jones Islamic Market U.S.
104	INDX	W1SGI	^W1SGI: Dow Jones Sustainability Worl
105	INDX	DJT	^DJT: Dow Jones Transportation Averag
106	INDX	DJUSM	^DJUSM: Dow Jones U.S. Mid-Cap Inde
107	INDX	W1XGA	^W1XGA: Dow Jones Sustainability Worl
108	INDX	DWC	^DWC: DJUS Market Index (full-cap
109	INDX	DJC	^DJC: Dow Jones-UBS Commodity Inde
110	INDX	IMXL	^IMXL: Dow Jones Islamic Market Titan
111	INDX	XLHK	^XLHK: Dow Jones Hong Kong Titans 30
112	INDX	DJTMDI	^DJTMDI: Dow Jones Media Titans 30 Inde
113	INDX	DJU	^DJU: Dow Jones Utility Averag
114	INDX	DWCOGS	^DWCOGS: Dow Jones U.S. Oil & Gas Tota
115	INDX	DJUSST	^DJUSST: Dow Jones U.S. Iron & Steel In
116	INDX	PSE	^PSE: NYSE Arca Tech 100 Index - New York Stock Exchange
117	INDX	DWCF	^DWCF: Dow Jones U.S. Total Stock Mar
118	INDX	W1SUS	^W1SUS: Dow Jones Sustainability Worl
119	INDX	DJASDT	^DJASDT: Dow Jones Asia Select Dividen
120	INDX	RCI	^RCI: Dow Jones Composite All REIT I
121	INDX	DJUSL	^DJUSL: Dow Jones U.S. Large-Cap Inde
122	INDX	P1DOW	^P1DOW: Dow Jones Asia/Pacific Inde
123	INDX	DJAT	^DJAT: Dow Jones Asian Titans 50 Inde
124	INDX	DJUS	^DJUS: Dow Jones U.S. Inde
125	INDX	DWMI	^DWMI: Dow Jones U.S. Micro-Cap Tota
126	INDX	DJUSS	^DJUSS: Dow Jones U.S. Small-Cap Inde
127	INDX	OMX	OMXS 30 Index (Sweden
128	INDX	STOXX50E	EuroStoxx 50 Inde
129	INDX	FTAS	FTSE All-Share Index (UK)
130	INDX	WIHUN_L	FTSE HUngary Index
131	INDX	WITUR_L	FTSE Turkey Index
132	INDX	WITHA_L	FTSE Thailand Index
133	INDX	WIPOL_L	FTSE Poland Index
134	INDX	WICZH_L	FTSE Czech Republic Index
135	INDX	OMXC20	OMX Copenhagen 20 Inde
136	INDX	IXE	^IXE: Select Sector Spdr-energy Inde
137	INDX	IXIC	NASDAQ Composite
138	INDX	SPEUP	S&P EUROPE 350"""
    df: typing.Union[None, pd.DataFrame] = pd.read_csv(StringIO(data), sep="\t")
    df: pd.DataFrame = df.set_index("ID")
    return df
