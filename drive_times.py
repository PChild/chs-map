from openrouteservice import distance_matrix
import openrouteservice
import pandas
import os

region = 'chs'

client = openrouteservice.Client(key=os.getenv('ORS_KEY'))

city_df = pandas.read_csv(region + '_city_locations.csv')
destination_data = []
for idx, row in city_df.iterrows():
    destination_data.append([row['lng'], row['lat']])

teams_df = pandas.read_csv(region + '_team_locations.csv')
source_data = []
for idx, row in teams_df.iterrows():
    source_data.append([row['lng'], row['lat']])

locations = source_data + destination_data
sources = list(range(len(source_data)))
destinations = list(range(len(source_data), len(source_data) + len(destination_data)))

dm_1 = distance_matrix.distance_matrix(client=client,
                                       locations=locations,
                                       sources=sources,
                                       destinations=destinations[:len(destinations)//2])

# dm_2 = distance_matrix.distance_matrix(client=client,
#                                       locations=locations,
#                                       sources=sources,
#                                       destinations=destinations[len(destinations)//2:])

print(dm_1)
