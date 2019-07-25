import requests
from datetime import datetime


class Charges:
    """
    The system tracks usage of paid service on an hourly basis.
    It doesn't track how much to charge for any particular product, but it will report for each instance,
    IP address and snapshot the amount of hours it's in use for.
    """

    def __init__(self, headers):
        self.headers = headers
        self.url = 'https://api.civo.com/v2/charges'

    def get(self, date_from: str = None, date_to: str = None) -> object:
        """
        Function to listing charges
        :param date_from: The from date like '2019-07-01'
        :param date_to: The to date like '2019-07-30'
        :return: object json
        """
        payload = {}

        if date_from:
            date = datetime.strptime(date_from, '%Y-%m-%d')
            payload['from'] = date.astimezone().isoformat()

        if date_to:
            date = datetime.strptime(date_to, '%Y-%m-%d')
            payload['to'] = date.astimezone().isoformat()

        r = requests.post(self.url, headers=self.headers, params=payload)

        return r.json()
