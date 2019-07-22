from shapely.geometry import Point
import matplotlib.pyplot as plt
import pandas as pd
import geopandas

region_name = 'CHS'
# region_name = 'New York'

if region_name == 'CHS':
    regions = ['Virginia', 'Maryland', 'District of Columbia']
else:
    regions = [region_name]
states = geopandas.read_file('states.json')
selected_states = states[states.NAME.isin(regions)]

teams_df = pd.read_csv(region_name + '_team_locations.csv')
team_locations = teams_df[['lng', 'lat']].apply(lambda row: Point(row['lng'], row['lat']), axis=1)
geo_locations = geopandas.GeoDataFrame({'geometry': team_locations, 'team_names': teams_df['team']})

center = geopandas.GeoDataFrame({'geometry': [Point(teams_df['lng'].mean(), teams_df['lat'].mean())]})
banners = geopandas.GeoDataFrame({'geometry': [Point(-77.47489126448296, 38.237303983134915)]})

# cities_df = pd.read_csv(region_name.lower() + '_city_locations.csv')
# city_locations = cities_df[['lng', 'lat']].apply(lambda row: Point(row['lng'], row['lat']), axis=1)
# cities = geopandas.GeoDataFrame({'geometry': city_locations})

fig, ax = plt.subplots(1, figsize=(15, 7))
base = selected_states.plot(ax=ax, color="white", edgecolor='black')
geo_locations.plot(ax=base, marker="o", markersize=25, edgecolor='black', alpha=0.5)
center.plot(ax=base, marker="*", markersize=255, color='yellow', edgecolor='black')
banners.plot(ax=base, marker="*", markersize=255, color='blue', edgecolor='black')

ax.set_title(region_name + ' Team Locations, CoM, and Banner CoM')
plt.axis('off')
plt.show()

