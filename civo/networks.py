import requests

from .utils import filter_list


class Networks:
    """
    To manage the private networks for an account, there are a set of APIs for listing them, as well as adding,
    renaming and removing them by ID.
    """

    def __init__(self, headers, api_url, region):
        param = "?region={region}".format(region=region) if region else ''
        self.headers = headers
        self.url = '{api_url}/v2/networks{param}'.format(api_url=api_url, param=param)

    def create(self, label: str) -> dict:
        """
        Function to create a private network
        :param label: a string that will be the displayed name/reference for the network.
        :return: object json
        """
        payload = {'label': label}
        r = requests.post(self.url, headers=self.headers, params=payload)

        return r.json()

    def search(self, filter: str = None) -> dict:
        """
        Function to listing the private networks
        :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                       you can filter by any object that is inside the json
        :return: [
                  {
                    "id": "50f2fffa-f81e-4e96-830f-e78f7e565e6f",
                    "name": "example-ltd-a775-development-75362452-562f-4b70-a65a-aeb4d4cd6864",
                    "region": "lon1",
                    "default": false,
                    "cidr": "0.0.0.0/0",
                    "label": "development"
                  }
                ]
        """
        r = requests.get(self.url, headers=self.headers)

        if filter:
            data = r.json()
            return filter_list(data=data, filter_by=filter)

        return r.json()

    def rename(self, id: str, label: str) -> dict:
        """
        Function to renaming a network
        :param id: id of the objects
        :param label: the new label to use.
        :return: object json
        """
        payload = {'label': label}
        r = requests.put(self.url + '/{}'.format(id), headers=self.headers, params=payload)

        return r.json()

    def delete(self, id: str) -> dict:
        """
        Function to removing a private network
        :return: object json
        """
        r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

        return r.json()
