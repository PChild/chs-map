from tqdm import tqdm
import geocoder
import pandas
import csv

region = 'chs'


def build_city_list():
    towns = [61, 162, 170, 172]
    min_size = 24000  # Sized to include all previous DCMP locations (Fairfax is smallest at 24.5k pop)
    if region is 'chs':
        states = ['va', 'md', 'dc']
    else:
        states = ['ny']

    '''Data from US Census Bureau City and Town Population Totals: 2010-2018
    https://www.census.gov/data/tables/time-series/demo/popest/2010s-total-cities-and-towns.html#ds
    '''
    valid_cities = []
    for state in states:
        state_df = pandas.read_csv(state + '.csv')
        valid_locations = state_df.loc[state_df.SUMLEV.isin(towns)]
        valid_locations = valid_locations.loc[valid_locations.POPESTIMATE2018 > min_size]
        valid_locations = valid_locations[['STNAME', 'NAME', 'POPESTIMATE2018']]
        valid_locations['NAME'] = valid_locations['NAME'].str.split(' ').str[:-1].str.join(' ')

        for idx, row in valid_locations.iterrows():
            valid_cities.append({'name': row.NAME, 'state': row.STNAME, 'pop': row.POPESTIMATE2018})

    return valid_cities


def save_city_list():
    cities = sorted(build_city_list(), key=lambda k: k['pop'], reverse=True)
    with open(region + '_city_names.csv', 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, ['name', 'state', 'pop'])
        writer.writeheader()

        prev_cities = []
        for city in cities:
            if city['name'] not in prev_cities:
                writer.writerow(city)
                prev_cities.append(city['name'])
    outfile.close()


def read_city_list():
    with open(region + '_city_names.csv', 'r') as infile:
        return [entry for entry in csv.DictReader(infile)]


def locate_city(city):
    lat, lng = geocoder.osm(city['name'] + ' ' + city['state']).latlng
    return {'name': city['name'], 'lat': lat, 'lng': lng}


def build_city_locations():
    city_locations = []
    for city in tqdm(read_city_list()):
        city_locations.append(locate_city(city))

    with open(region + '_city_locations.csv', 'w') as outfile:
        writer = csv.DictWriter(outfile, ['name', 'lat', 'lng'])
        writer.writeheader()

        for city in city_locations:
            writer.writerow(city)


if __name__ == '__main__':
    build_city_locations()

