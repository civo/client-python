import requests
from .utils import filter_list


class LoadBalance:
    """
    If you want to create a load balancer for your instances, to spread your web traffic
    between them then you can easily launch a managed load balancer service on Civo.
    """

    def __init__(self, headers):
        self.headers = headers
        self.url = 'https://api.civo.com/v2/loadbalancers'

    def create(self):
        return 'No implemeted yet'

    def lists(self, filter: str = None) -> dict:
        """
        Function to list load balancers
        :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                       you can filter by any object that is inside the json
        :return: object json
        """
        r = requests.get(self.url, headers=self.headers)

        if filter:
            data = r.json()
            return filter_list(data=data, filter=filter)

        return r.json()

    def delete(self, id: str) -> dict:
        """
        Function to deleting a load balancer
        :param id: ID of the load balancer to delete
        :return: object json
        """
        r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

        return r.json()
