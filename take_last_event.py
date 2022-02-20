import requests
from json.decoder import JSONDecodeError
from datetime import date, timedelta
import calendar
from datetime import datetime
import pytz
from bs4 import BeautifulSoup as bs
import requests
import os.path as path
import re
from PIL import Image
from urllib.request import urlopen
from io import BytesIO
import json
import os


# Date in New York
today = datetime.now(pytz.timezone('America/New_York')).date()
ten_days_ago = today - timedelta(days=10)
# Request to API, last 30 days
try:
    # startDate: default to 30 days prior to current UTC date
    # endDate: default to current UTC date
    params = {'startDate': ten_days_ago,
     #        'endDate': '2017-09-07'
             }

    url = 'https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/CME?'
    r = requests.get(url, params) # , params
    data = r.json()
 #   print(f'Number of CME in the 10 days prior to current date: {len(data)}')
except ValueError: # includes simplejson.decoder.JSONDecodeError
    print('Something was wrong in the API request process!:(')

# Last Event
last_cme = data[-1] #-1


if os.path.exists(f"last_100_events/{last_cme['activityID']}.json"):
    print('STILL NO NEW EVENTS')
else:
    print(f"NEW EVENT: {last_cme['activityID']}")
    # Save event data
    with open(f"last_100_events/{last_cme['activityID']}.json", "w") as file:
        json.dump(last_cme, file)

