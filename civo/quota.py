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

    def get(self,name:str = None) -> dict:
        """
        Function to get quota
        :param name: to get quota for a given account name if api key is of a system account(optional)
        :return: object json
        """
        params = {}
        if name:
            params = {"name":name}
        r = requests.get(self.url, headers=self.headers,params=params)

        return r.json()
