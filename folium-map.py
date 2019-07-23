from folium.plugins import Search
import event_types
import geocoder
import random
import folium
import base64
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


def encode_image(src, url):
    img_data = base64.b64encode(open('./img/' + src + '.png', 'rb').read()).decode('UTF-8')
    img_html = '<a target="_blank" rel="noopener noreferrer" href= "{}">' \
               '<img src="data:image/png;base64,{}" style="padding: 1px"></a>'.format
    return img_html(url, img_data)


def prof_url(src, end):
    return 'https://www.' + src + '.com/' + end


def process_social(tm):
    social = tba.team_profiles(tm.team_number)

    social_data = encode_image('tba', 'https://www.thebluealliance.com/team/' + str(tm.team_number))
    for profile in social:
        form = profile['type'][:-8]
        url = prof_url(form, profile['foreign_key'])
        social_data += encode_image(form, url)
    if team.website:
        social_data += encode_image('website', team.website)
    return social_data


def style_function(i):
    return {
        'fillOpacity': 0.07,
        'weight': 2,
        'color': '#000',
        'fillColor': '#000'
    }


# Base map settings
m = folium.Map(location=[mid_lat, mid_lng],
               zoom_start=8,
               tiles=None)
folium.TileLayer(tiles='OpenStreetMap', control=False).add_to(m)

# Add shapes
folium.GeoJson(
    region + '.json',
    control=False,
    style_function=style_function,
    overlay=False
).add_to(m)

body = '<html><body style="padding: 0; margin:0">{}</body></html>'.format
paragraph = '<p style="margin: 1px; padding: 1px; font-size: small; font-family: sans-serif;">{}</p>'.format

# Add team layer and inactive team layers
team_layer = folium.plugins.MarkerCluster(name='Current Teams').add_to(m)
gone_layer = folium.plugins.MarkerCluster(name='Former Teams', show=False).add_to(m)

# Read in Nate's more precise location data
nate_data = pandas.read_csv('nate_locs.csv')
current_teams = tba.district_teams(year + region)

for idx, row in nate_data.iterrows():
    team_data = [item for item in current_teams if item['team_number'] == row['team']]
    is_active = len(team_data) > 0

    if is_active:
        team = team_data[0]
        ico_color = 'blue'
        ico = 'fa-users'
    else:
        team = tba.team(row['team'])
        ico_color = 'red'
        ico = 'times'

    line_1 = paragraph('Team ' + str(team.team_number))
    line_2 = paragraph(team.nickname)
    line_3 = paragraph(team.city + ', ' + team.state_prov)
    line_4 = process_social(team)
    html = body(line_1 + line_2 + line_3 + line_4)

    team_inf = nate_data[nate_data['team'] == team.team_number].iloc[0]
    team_str = str(team.team_number)

    team_marker = folium.Marker(location=[team_inf['lat'], team_inf['lng']],
                                tooltip=team.team_number,
                                icon=folium.Icon(icon=ico, color=ico_color, prefix='fa'),
                                popup=folium.Popup(html, min_width=180, max_width=2000)
                                )
    if is_active:
        team_marker.add_to(team_layer)
    else:
        team_marker.add_to(gone_layer)

# Add mean location of teams
mean_loc = folium.FeatureGroup(name='Mean Location', show=False)
folium.Marker(location=[teams_df['lat'].mean(), teams_df['lng'].mean()],
              icon=folium.Icon(color='orange', icon='plus'),
              tooltip='Teams Mean Location').add_to(mean_loc)
mean_loc.add_to(m)

# Add district events
for yr in range(int(year) - 3, int(year) + 1):
    is_last = yr == int(year)
    yr_group = folium.FeatureGroup(name=str(yr) + ' Events', show=is_last)
    for event in tba.district_events(str(yr) + region):
        lat, lng = geocoder.google(event.address).latlng

        is_dist = event.event_type is event_types.DISTRICT
        ico = 'cog' if is_dist else 'star'
        ico_color = 'green' if is_dist else 'orange'

        line_1 = paragraph(event.name)
        line_2 = paragraph('Week ' + str(event.week))
        line_3 = paragraph(event.location_name)
        line_4 = paragraph(event.address)
        line_5 = encode_image('tba', 'https://www.thebluealliance.com/event/' + event.key)
        line_5 += encode_image('twitch', 'https://www.twitch.tv/' + event.webcasts[0]['channel'])
        line_5 += encode_image('website', event.website)

        html = body(line_1 + line_2 + line_3 + line_4 + line_5)

        event_marker = folium.Marker(location=[lat, lng],
                                     tooltip=event.key,
                                     icon=folium.Icon(icon=ico, color=ico_color),
                                     popup=folium.Popup(html, min_width=240, max_width=2000))
        event_marker.add_to(yr_group)
    yr_group.add_to(m)

# Add layer controls
folium.LayerControl().add_to(m)

legend_html = '''
     <div style="position: fixed; bottom: 25px; right: 10px; width: 120px; height: 120px; border:2px solid grey; 
     z-index:9999; font-size:12px; background:#eee">
     <div style="margin: 5px 0 0 5px">Active Team <i class="fa fa-users" style="color:white; background-color:#37A7DA; font-size: 1.2em;
      margin:2px; padding: 0; position:absolute; right:2px"></i></div>
     <div style="margin: 5px 0 0 5px"> Former Team <i class="fa fa-times" style="color:white; background-color:#D33D29; font-size: 1.5em;
      margin:2px; padding: 0; position:absolute; right:2px"></i><br></div>
     <div style="margin: 5px 0 0 5px"> Mean Location <i class="fa fa-plus" style="color:white; background-color:#F69730; font-size: 1.5em;
      margin:2px; padding: 0; position:absolute; right:2px"></i><br></div>
     <div style="margin: 5px 0 0 5px"> District Event <i class="fa fa-cog" style="color:white; background-color:#71AE26; font-size: 1.5em;
      margin:2px; padding: 0; position:absolute; right:2px"></i><br></div>
     <div style="margin: 5px 0 0 5px"> District Champs <i class="fa fa-star" style="color:white; background-color:#F69730; font-size: 1.3em;
      margin:2px; padding: 0; position:absolute; right:2px"></i></div>
      </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))
m.save('map.html')
