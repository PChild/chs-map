import pandas

'''Data from US Census Bureau City and Town Population Totals: 2010-2018
https://www.census.gov/data/tables/time-series/demo/popest/2010s-total-cities-and-towns.html#ds
'''

towns = [61, 71, 162, 170, 172]
min_size = 24000 # Sized to include all previous DCMP locations (Fairfax is smallest at 24.5k pop)
regions = ['virginia', 'maryland', 'dc']

if __name__ == '__main__':
    for region in regions:
        region_df = pandas.read_csv(region + '.csv')
        valid_locations = region_df.loc[region_df.SUMLEV.isin(towns)]
        valid_locations = valid_locations.loc[valid_locations.POPESTIMATE2018 > min_size]
        valid_locations = valid_locations[['STNAME', 'NAME', 'POPESTIMATE2018']]
        valid_locations['NAME'] = valid_locations['NAME'].str[:-5]
        print(region, len(valid_locations), 'valid locations:')
        print(valid_locations)
