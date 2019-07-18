import folium
import pandas
import tbapy
import os

tba = tbapy.TBA(os.getenv('TBA_KEY'))

region = 'chs'
year = '2019'

teams_df = pandas.read_csv(region + '_team_locations.csv')
mid_lat = teams_df['lat'].min() + (teams_df['lat'].max() - teams_df['lat'].min()) / 2
mid_lng = teams_df['lng'].min() + (teams_df['lng'].max() - teams_df['lng'].min()) / 2


def style_function(feature):
    return {
        'fillOpacity': 0.07,
        'weight': 2,
        'color': '#000',
        'fillColor': '#000'
    }


m = folium.Map(location=[mid_lat, mid_lng],
               zoom_start=7)

folium.GeoJson(
    region + '.json',
    name='geojson',
    style_function=style_function
).add_to(m)

for team in tba.district_teams(year + region):
    team_loc = teams_df[teams_df['team'] == team.team_number].iloc[0]
    line_1 = str(team.team_number) + ' - ' + team.nickname + '<br>'
    line_2 = team.city + ', ' + team.state_prov + '<br>'
    popup = folium.Html(line_1 + line_2, script=True)
    folium.Marker(
        location=[team_loc['lat'], team_loc['lng']],
        popup=popup,
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

m.save('index.html')
