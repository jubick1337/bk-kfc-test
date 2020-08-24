import pickle
from collections import defaultdict

import pandas as pd
from csv_to_geojson import create_geojson

from analysis.utils import Point, distance, Store

bk_df = pd.read_csv('../results/bk_moscow.csv')
kfc_df = pd.read_csv('../results/kfc_moscow.csv')
near_concurrents = defaultdict(int)

kfc_stores = [Store(row[1]['store_id'], Point(row[1]['lat'], row[1]['lon'])) for row in kfc_df.iterrows()]

for bk_store in bk_df.iterrows():
    store_id = bk_store[1]['store_id']
    store_point = Point(bk_store[1]['lat'], bk_store[1]['lon'])
    bk_store = Store(store_id, store_point)

    for kfc_store in kfc_stores:
        if distance(bk_store.location, kfc_store.location) < 2000.0:
            near_concurrents[bk_store] += 1

result = {k: v for k, v in sorted(near_concurrents.items(), key=lambda item: item[1])}

geojson = pd.DataFrame.from_dict(
    {store.id: [store.location.lat, store.location.lon, result[store]] for store in result},
    orient='index').reset_index()

geojson.columns = ['id', 'lng', 'lat', 'count']

geojson.to_csv('../results/result.csv', index=False)
create_geojson('../results/result.csv')

with open('../results/near_concurrents.bin', 'wb+') as file:
    pickle.dump(result, file)
