import requests


class Quota:
    """
    Our quotas (and therefore our pricing), are based on a combined allocation of CPU, RAM and disk.
    All customers start on a basic quota level and after a period of proving that the quota is being
    handled correctly or after a call to our offices, we can increase this quota.
    """

    def __init__(self, headers, api_url):
        self.headers = headers
        self.url = '{}/v2/quota'.format(api_url)

    def get(self) -> dict:
        """
        Function to get quota
        :return: object json
        """
        r = requests.post(self.url, headers=self.headers)

        return r.json()
