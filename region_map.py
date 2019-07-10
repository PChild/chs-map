import matplotlib.pyplot as plt
from retrying import retry
import geopandas
import requests


@retry(wait_fixed=5000)
def get_route(coords):
    ans = requests.get("http://router.project-osrm.org/route/v1/driving/" + coords + "?overview=full").json()
    if ans is None or ans == {'message': 'Too Many Requests'}:
        raise Exception("Too Many Requests")
    return ans

# TODO add city list
# TODO rest of the owl


states = geopandas.read_file('states.json')
chs_states = ['Virginia', 'Maryland', 'District of Columbia']

selected_states = states[states.NAME == 'New York']
ax = selected_states.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
plt.show()
