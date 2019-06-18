import geocoder
import tbapy
import csv
import os

year = 2019
dist = 'chs'


def locate_team(tm):
    lat, lng = geocoder.osm(tm.city + ' ' + tm.state_prov).latlng
    return {'team': tm.team_number, 'lat': lat, 'lng': lng}


if __name__ == '__main__':
    dist_str = str(year) + dist
    tba = tbapy.TBA(os.getenv('TBA_KEY'))
    dist_teams = tba.district_teams(dist_str)
    dist_keys = [item.key for item in dist_teams]

    dist_locs = {}
    with open('team_locations.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'frc' + row['team'] in dist_keys:
                dist_locs['frc' + str(row['team'])] = row
    file.close()

    # Handle when there are teams that weren't in the base csv.
    for team in dist_teams:
        if team.key not in dist_locs:
            dist_locs[team.key] = locate_team(team)

    with open(dist_str + '_locations.csv', 'w', newline='') as outfile:
        fieldnames = ['team', 'lat', 'lng']
        writer = csv.DictWriter(outfile, fieldnames)
        writer.writeheader()

        for team in dist_locs:
            writer.writerow(dist_locs[team])
    outfile.close()
