import requests

from .utils import filter_list


class Volumes:
    """
    We provide a flexible size additional storage service for our Instances called volumes.
    This creates and attaches an additional virtual disk to the instance, allowing you to put backups or database
    files on the separate volume and later move the volume to another instance.

    As volume storage is chargeable, at any time these can be deleted.
    """

    def __init__(self, headers, api_url, region):
        param = "?region={region}".format(region=region) if region else ''
        self.headers = headers
        self.url = '{api_url}/v2/volumes{param}'.format(api_url=api_url, param=param)

    def create(self, name: str, size_gb: str, bootable: str = 'false') -> dict:
        """
        Function to create a new volume
        :param name: A name that you wish to use to refer to this volume (required)
        :param size_gb: A minimum of 1 and a maximum of your available disk space from your quota specifies
                        the size of the volume in gigabytes (required).
        :param bootable: Mark the volume as bootable with a boolean (optional; defaults to false).
        :return: objects json
        """
        payload = {'name': name, 'size_gb': size_gb}

        if bootable:
            payload['bootable'] = bootable

        r = requests.post(self.url, headers=self.headers, params=payload)

        return r.json()

    def search(self, filter: str = None) -> dict:
        """
        Function to list volumes
        :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                       you can filter by any object that is inside the json
        :return: object json
        """
        r = requests.get(self.url, headers=self.headers)

        if filter:
            data = r.json()
            return filter_list(data=data, filter_by=filter)

        return r.json()

    def resizing(self, id: str, size_gb: str) -> dict:
        """
        Function to resizing a volume
        :param id: id of the objects
        :param size_gb: A minimum of the existing size of the volume plus 1 and a maximum of your available
                        disk space from your quota specifies the size of the volume in gigabytes (required).
        :return: object json
        """
        payload = {'size_gb': size_gb}

        r = requests.put(self.url + '/{}/resize'.format(id), headers=self.headers, params=payload)

        return r.json()

    def attach(self, id: str, instance_id: str) -> dict:
        """
        Function to attach a volume to an instance
        :param id: id of the objects
        :param instance_id: The ID of an instance that you wish to attach this volume to (required)
        :return: object json
        """
        payload = {'instance_id': instance_id}

        r = requests.put(self.url + '/{}/attach'.format(id), headers=self.headers, params=payload)

        return r.json()

    def detach(self, id: str) -> dict:
        """
        Function to detach a volume from an instance
        :param id: id of the objects
        :return: object json
        """
        r = requests.put(self.url + '/{}/detach'.format(id), headers=self.headers)

        return r.json()

    def delete(self, id: str) -> dict:
        """
        Function to deleting a volume
        :param id: name of the instance
        :return: object json
        """
        r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

        return r.json()