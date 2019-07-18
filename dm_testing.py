import pandas
import json

region = 'chs'

teams_df = pandas.read_csv(region + '_team_locations.csv')
city_df = pandas.read_csv(region + '_city_locations.csv')

with open('dm_test.json') as f:
    dm_packet = json.load(f)
dist_matrix = pandas.DataFrame(dm_packet['durations'])
dist_matrix = dist_matrix[~dist_matrix[1].str.contains('None', na=False)]

# print(dist_matrix.iloc[3])
# print(teams_df.iloc[3])
# print(city_df)

for idx, item in city_df['name'][:len(city_df['name'])//2].iteritems():
    print(item, ': ', round(dist_matrix[idx].mean()/3600, 2), "hours avg drive time")

# print(dist_matrix[dist_matrix[2] == "None"])
#print(teams_df.iloc[77])
