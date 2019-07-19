import random
import folium
import pandas
import tbapy
import os

tba = tbapy.TBA(os.getenv('TBA_KEY'))

region = 'chs'
year = '2019'

random.seed(year + region)

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
               zoom_start=8,
               tiles=None)

folium.TileLayer(tiles='OpenStreetMap', control=False).add_to(m)

folium.GeoJson(
    region + '.json',
    control=False,
    style_function=style_function,
    overlay=False
).add_to(m)

team_set = folium.FeatureGroup(name='Teams')
seen_list = []
for team in tba.district_teams(year + region):
    team_inf = teams_df[teams_df['team'] == team.team_number].iloc[0]
    team_loc = [team_inf['lat'], team_inf['lng']]

    # if location value is non-unique then jitter it
    if team_loc in seen_list:
        print('jittered', team.team_number)
        team_loc = [team_loc[0] + random.uniform(-0.01, 0.01),
                    team_loc[1] + random.uniform(-0.01, 0.01)]
    seen_list.append(team_loc)

    line_1 = '<p>' + str(team.team_number) + ' ' + team.nickname + '</p>'
    line_2 = '<p>' + team.city + ', ' + team.state_prov + '</p>'

    line_3 = ''



    html = line_1 + line_2
    popup = folium.Popup(folium.IFrame(html=html, width=250, height=50), max_width=2000)

    folium.Marker(
        location=team_loc,
        popup=html,
        icon=folium.Icon(icon='cog'),
        tooltip=str(team.team_number)
    ).add_to(team_set)
team_set.add_to(m)

mean_loc = folium.FeatureGroup(name='Mean Location')
folium.Marker(location=[teams_df['lat'].mean(), teams_df['lng'].mean()],
              icon=folium.Icon(color='orange', icon='star'),
              tooltip='Mean location').add_to(mean_loc)
mean_loc.add_to(m)

folium.LayerControl().add_to(m)

m.save('index.html')
