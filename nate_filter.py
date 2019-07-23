import geopandas
import tbapy
import os

tba = tbapy.TBA(os.getenv('TBA_KEY'))

chs_teams = [int(team[3:]) for team in tba.district_teams('2019chs', keys=True)]

test = geopandas.read_file('nate_chs.geojson')
test['team'] = test['name'].str.split(' ').str[0]
teams_df = test[test['team'].str.isnumeric()]
teams_df['team'] = teams_df['team'].astype(int)
teams_df['lat'] = teams_df['geometry'].y
teams_df['lng'] = teams_df['geometry'].x
teams_df['active'] = teams_df['team'].isin(chs_teams)
teams_out = teams_df[['team', 'lat', 'lng', 'active']]
teams_out.to_csv('nate_locs.csv', index=False)
# print(teams_out)
