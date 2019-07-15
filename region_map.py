from shapely.geometry import Point
import matplotlib.pyplot as plt
from retrying import retry
import pandas as pd
import geopandas
import requests


@retry(wait_fixed=5000)
def get_route(coords):
    ans = requests.get("http://router.project-osrm.org/route/v1/driving/" + coords + "?overview=full").json()
    if ans is None or ans == {'message': 'Too Many Requests'}:
        raise Exception("Too Many Requests")
    return ans

# TODO add city list
# TODO rest of the owl

region_name = 'CHS'
#region_name = 'New York'

if region_name == 'CHS':
    regions = ['Virginia', 'Maryland', 'District of Columbia']
else:
    regions = [region_name]
states = geopandas.read_file('states.json')
selected_states = states[states.NAME.isin(regions)]

teams_df = pd.read_csv(region_name + '_locations.csv')
team_locations = teams_df[['lng', 'lat']].apply(lambda row: Point(row['lng'], row['lat']), axis=1)
geo_locations = geopandas.GeoDataFrame({'geometry': team_locations, 'team_names': teams_df['team']})

center = geopandas.GeoDataFrame({'geometry': [Point(teams_df['lng'].mean(), teams_df['lat'].mean())]})

fig, ax = plt.subplots(1, figsize=(15, 7))
base = selected_states.plot(ax=ax, color="white", edgecolor='black')
geo_locations.plot(ax=base, marker="o", markersize=55, edgecolor='black', alpha=0.5)
center.plot(ax=base, marker="*", markersize=255, color='yellow', edgecolor='black')


ax.set_title(region_name + ' Team Locations and Center of Mass')
plt.axis('off')
plt.show()

