import json

import pandas as pd
import requests

api_url = 'https://api.kfc.com/api/store/v2/store.geo_search'
payload = {"coordinates": [55.73135910527806, 37.59104925054579], "radiusMeters": 30000, "channel": "website"}
headers = {'content-type': 'application/json'}

kfc_response = requests.post(api_url, data=json.dumps(payload), headers=headers)
kfc_json_data = kfc_response.json()['searchResults']
kfc_moscow_data = dict()

for data in kfc_json_data:
    store_contacts = data['store']['contacts']
    if store_contacts['city']['en'] == 'Moscow':
        store_coordinates = store_contacts['coordinates']['geometry']['coordinates']
        kfc_moscow_data[data['store']['storeId']] = (store_coordinates[0], store_coordinates[1])


df = pd.DataFrame.from_dict(kfc_moscow_data, orient='index', ).reset_index()
df.columns = ['store_id', 'lat', 'lon']

df.to_csv('../results/kfc_moscow.csv', index=False)
