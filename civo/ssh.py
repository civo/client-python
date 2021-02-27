import requests

from .utils import filter_list


class Ssh:
    """
    To manage the SSH keys for an account that are used for logging in to instances,
    there are a set of APIs for listing the SSH public keys currently stored,
    as well as adding and removing them by name.
    """

    def __init__(self, headers, api_url):
        self.headers = headers
        self.url = '{}/v2/sshkeys'.format(api_url)

    def create(self, name: str, public_key: str) -> dict:
        """
        Function to uploading a SSH public key
        :param name: Name of the key
        :param public_key: Public key of the ssh
        :return: object json
        """
        payload = {'name': name, 'public_key': public_key}
        r = requests.post(self.url, headers=self.headers, params=payload)

        return r.json()

    def search(self, filter: str = None) -> dict:
        """
        Function to listing the SSH public keys
        :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                       you can filter by any object that is inside the json
        :return: object json
        """
        r = requests.get(self.url, headers=self.headers)

        if filter:
            data = r.json()
            return filter_list(data=data, filter_by=filter)

        return r.json()

    def retrieving(self, id: str) -> dict:
        """
        Function to retrieving a SSH key
        :param id: id of the objects
        :return: object json
        """
        r = requests.get(self.url + '/{}'.format(id), headers=self.headers)

        return r.json()

    def updating(self, id: str, name: str) -> dict:
        """
        Function to updating a SSH key
        :param id: id of the objects
        :param name: name to change
        :return: object json
        """
        payload = {'name': name}
        r = requests.put(self.url + '/{}'.format(id), headers=self.headers, params=payload)

        return r.json()

    def delete(self, id: str) -> dict:
        """
        Function to removing a SSH key
        :return: object json
        """
        r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

        return r.json()
