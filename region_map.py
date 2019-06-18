from retrying import retry
import requests


@retry(wait_fixed=5000)
def get_route(coords):
    ans = requests.get("http://router.project-osrm.org/route/v1/driving/" + coords + "?overview=full").json()
    if ans is None or ans == {'message': 'Too Many Requests'}:
        raise Exception("Too Many Requests")
    return ans

# TODO add city list
# TODO rest of the owl