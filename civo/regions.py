import requests

from .utils import filter_list


class Regions:
    """
    Civo will be hosted in multiple datacentres (a.k.a. regions), with more coming online all the time.
    You can choose when creating an instance which region to have it hosted in (necessary if you want to
    share a private network between your instances) - or you can leave it for Civo to allocate you to a
    region if you don't care.
    """

    def __init__(self, headers, api_url):
        self.headers = headers
        self.url = '{}/v2/regions'.format(api_url)

    def search(self, filter: str = None) -> dict:
        """
        Function to listing available regions
        :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                       you can filter by any object that is inside the json
        :return: object json
        """
        r = requests.get(self.url, headers=self.headers)

        if filter:
            data = r.json()
            return filter_list(data=data, filter_by=filter)

        return r.json()
