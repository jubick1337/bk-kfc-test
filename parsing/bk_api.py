import os
import time

import pandas as pd
import requests

bk_response = requests.get('https://burgerking.ru/restaurant-locations-json-reply-new/')
bk_json_data = bk_response.json()
bk_moscow_data = dict()

for data in bk_json_data:
    request = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={data["latitude"]},{data["longitude"]}&key={os.environ["GOOGLE_API_KEY"]}'
    try:
        response = requests.get(request).json()
        for result in response['results']:
            for address_component in result['address_components']:
                if address_component['long_name'] == 'Moscow':
                    bk_moscow_data[data['storeId']] = (data['latitude'], data['longitude'])
    except:
        time.sleep(5)
        response = requests.get(request).json()
        for result in response['results']:
            for address_component in result['address_components']:
                if address_component['long_name'] == 'Moscow':
                    bk_moscow_data[data['storeId']] = (data['latitude'], data['longitude'])

df = pd.DataFrame.from_dict(bk_moscow_data, orient='index').reset_index()
df.columns = ['store_id', 'lat', 'lon']

df.to_csv('../results/bk_moscow.csv', index=False)
