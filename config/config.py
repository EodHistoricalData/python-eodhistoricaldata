from decouple import config

class Config:
    EOD_HISTORICAL_DATA_API_KEY_ENV_VAR: str = config('eod_api_key')
    EOD_HISTORICAL_DATA_API_KEY_DEFAULT: str = config('eod_api_key')
    EOD_HISTORICAL_DATA_API_URL: str = "https://eodhistoricaldata.com/api"
