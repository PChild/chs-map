import geopandas

test = geopandas.read_file('nate_chs.geojson')
test['team'] = test['name'].str.split(' ').str[0]
teams_df = test[test['team'].str.isnumeric()]
teams_df['lat'] = teams_df['geometry'].y
teams_df['lng'] = teams_df['geometry'].x
teams_out = teams_df[['team', 'lat', 'lng']]
teams_out.to_csv('nate_locs.csv', index=False)
print(teams_out)
