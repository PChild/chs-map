from tqdm import tqdm
import geocoder
import tbapy
import csv
import os


def get_region_teams(desired_region, year=2019, is_dist=False):
    if is_dist:
        return [item.team_number for item in tba.district_teams(str(year) + desired_region[0])]

    teams = []
    for page in range(32):
        for tm in tba.teams(page, year):
            if tm.state_prov in desired_region:
                teams.append(tm.team_number)

    return teams


def locate_team(tm):
    tem = tba.team(tm)
    lat, lng = geocoder.osm(tem.city + ' ' + tem.state_prov).latlng
    return {'team': tm, 'lat': lat, 'lng': lng}


if __name__ == '__main__':
    tba = tbapy.TBA(os.getenv('TBA_KEY'))

    region = ['New York']
    region_teams = get_region_teams(region)

    team_locs = {}
    with open('team_locations.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if str(row['team']) in region_teams:
                team_locs[str(row['team'])] = row
    file.close()

    # Handle when there are teams that weren't in the base csv.
    for team in tqdm(region_teams):
        if str(team) not in team_locs:
            team_locs[str(team)] = locate_team(team)

    with open(region[0] + '_locations.csv', 'w', newline='') as outfile:
        fieldnames = ['team', 'lat', 'lng']
        writer = csv.DictWriter(outfile, fieldnames)
        writer.writeheader()

        for team in team_locs:
            writer.writerow(team_locs[team])
    outfile.close()
