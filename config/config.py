from decouple import config
import os
class Config:
    EOD_HISTORICAL_DATA_API_KEY_ENV_VAR: str = os.getenv('EOD_HISTORICAL_API_KEY') or config('EOD_HISTORICAL_API_KEY')
    EOD_HISTORICAL_DATA_API_KEY_DEFAULT: str = os.getenv('EOD_HISTORICAL_API_KEY') or config('EOD_HISTORICAL_API_KEY')
    EOD_HISTORICAL_DATA_API_URL: str = "https://eodhistoricaldata.com/api"
