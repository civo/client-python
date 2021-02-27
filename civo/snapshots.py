import requests

from .utils import filter_list


class Snapshots:
    """
    We provide a backup service for our Instances called snapshots. This takes an exact copy of the instance's
    virtual hard drive. At any point an instance can be restored to the state it was in when the snapshot was made.
    These snapshots can also be used to build a new instance to scale identically configured infrastructure.

    As snapshot storage is chargeable, at any time these can be deleted. They can also be scheduled rather than
    immediately created, and if desired repeated at the same schedule each week (although the repeated snapshot
    will overwrite itself each week not keep multiple weekly snapshots).
    """

    def __init__(self, headers, api_url, region):
        param = "?region={region}".format(region=region) if region else ''
        self.headers = headers
        self.url = '{api_url}/v2/snapshots{param}'.format(api_url=api_url, param=param)

    def create(self, name: str, instance_id: str, safe: str = 'false', cron_timing: str = None) -> dict:
        """
        Function to create a new or update an old snapshot
        :param instance_id: The ID of the instance to snapshot
        :param name: The name of the instance
        :param safe: If true the instance will be shut down during the snapshot to ensure all files are in a
                     consistent state (e.g. database tables aren't in the middle of being optimised and hence
                     risking corruption). The default is false so you experience no interruption of service,
                     but a small risk of corruption.
        :param cron_timing: If a valid cron string is passed, the snapshot will be saved as an automated snapshot,
                            continuing to automatically update based on the schedule of the cron sequence provided.
                            The default is nil meaning the snapshot will be saved as a one-off snapshot.
        :return: objects json
        """
        payload = {'instance_id': instance_id}

        if safe:
            payload['safe'] = safe

        if cron_timing:
            payload['cron_timing'] = cron_timing

        r = requests.put(self.url + '/{}'.format(name), headers=self.headers, params=payload)

        return r.json()

    def search(self, filter: str = None) -> dict:
        """
        Function to list snapshots
        :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                       you can filter by any object that is inside the json
        :return: object json
        """
        r = requests.get(self.url, headers=self.headers)

        if filter:
            data = r.json()
            return filter_list(data=data, filter_by=filter)

        return r.json()

    def delete(self, name: str) -> dict:
        """
        Function to deleting a snapshot
        :param name: name of the instance
        :return: object json
        """
        r = requests.delete(self.url + '/{}'.format(name), headers=self.headers)

        return r.json()
