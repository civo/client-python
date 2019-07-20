import os
import requests


class Civo:

    def __init__(self, civo_token=None):
        # Get token from env or pass to the class
        if not civo_token:
            self.token = os.getenv('CIVO_TOKEN', False)
        else:
            self.token = civo_token

        # Create headers for all requests to civo api
        if not self.token:
            raise Exception('CIVO_TOKEN not found in the enviroment')

        self.headers = {'Authorization': 'bearer {}'.format(self.token)}

        # Ssh class
        self.ssh = self.Ssh(self.headers)

    class Ssh:

        def __init__(self, headers):
            self.headers = headers
            self.url = 'https://api.civo.com/v2/sshkeys'

        def uploading(self, name: str, public_key: str) -> object:
            """
            Function to uploading a SSH public key
            :param name: Name of the key
            :param public_key: Public key of the ssh
            :return: object json
            """
            payload = {'name': name, 'public_key': public_key}
            r = requests.post(self.url, headers=self.headers, params=payload)

            return r.json()

        def listing(self) -> object:
            """
            Function to listing the SSH public keys
            :return: object json
            """
            r = requests.get(self.url, headers=self.headers)

            return r.json()

        def retrieving(self, id: str) -> object:
            """
            Function to retrieving a SSH key
            :param id: id of the objects
            :return: object json
            """
            r = requests.get(self.url + '/{}'.format(id), headers=self.headers)

            return r.json()

        def updating(self, id: str, name: str) -> object:
            """
            Function to updating a SSH key
            :param id: id of the objects
            :param name: name to change
            :return: object json
            """
            payload = {'name': name}
            r = requests.put(self.url + '/{}'.format(id), headers=self.headers, params=payload)

            return r.json()

        def removing(self, id: str) -> object:
            """
            Function to removing a SSH key
            :return: object json
            """
            r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

            return r.json()