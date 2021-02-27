import requests

from .utils import filter_list


class Size:
    """
    Instances are sized by combinations of CPU virtual cores, memory and disk space.
    Custom sizes can also be created by customers, as our quotas and therefore pricing are based on
    a combined allocation of CPU, RAM and disk.
    """

    def __init__(self, headers, api_url):
        self.headers = headers
        self.url = '{}/v2/sizes'.format(api_url)

    def search(self, filter: str = None) -> dict:
        """
        Function to listing available instances sizes
        :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                       you can filter by any object that is inside the json
        :return: object json
        """
        r = requests.get(self.url, headers=self.headers)

        if filter:
            data = r.json()
            return filter_list(data=data, filter_by=filter)

        return r.json()
