import os
import requests
import pandas as pd
from dotenv import load_dotenv


"""Load env variables"""
load_dotenv()

"""Get env variables"""
FRIDGEWATCHDOG_API_KEY = os.getenv('FRIDGEWATCHDOG_API_KEY')
API_SERVER = os.getenv('API_SERVER')
ENDPOINT = "/get"

"""Create URL for fetching data"""
URL = f"{API_SERVER}{ENDPOINT}"

"""Create parameters for API"""
params = {
    'code': FRIDGEWATCHDOG_API_KEY
}

"""Request API for data"""
response = requests.get(url=URL, params=params)

if response.status_code not in [200, 201]:
    raise requests.exceptions.ConnectionError("Response without status code 200 or 201")

data = response.json()
df = pd.json_normalize(data)








print()