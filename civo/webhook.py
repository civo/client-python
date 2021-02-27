import requests

from .utils import filter_list


class WebHook:
    """
    Open certain actions taking place within your account, we can trigger a JSON POST callback to a URL or your choice.
    """

    def __init__(self, headers, api_url):
        self.headers = headers
        self.url = '{}/v2/webhooks'.format(api_url)

    def create(self, events: str, url: str, secret: str = None) -> dict:
        """
        Function to create a new webhook
        :param events: This is a list of events that the webhook should be triggered for.
                       Alternative you can use a list containing a single entry of "*" to signify trigger for all events. (required)
        :param url: This is the URL to send the webhook to (required).
        :param secret: This is if you want to specify your own secret, if not a random one will be created for you (optional).
        :return: object json
        """
        payload = {'events': events, 'url': url}

        if secret:
            payload['secret'] = secret

        r = requests.post(self.url, headers=self.headers, params=payload)

        return r.json()

    def search(self, filter: str = None) -> dict:
        """
        Function to listing webhooks
        :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                       you can filter by any object that is inside the json
        :return: object json
        """

        r = requests.get(self.url, headers=self.headers)

        if filter:
            data = r.json()
            return filter_list(data=data, filter_by=filter)

        return r.json()

    def test(self, id: str) -> dict:
        """
        Function to test a webhook
        :param id: id of webhook object
        :return: object json
        """
        r = requests.post(self.url + '/{}/test'.format(id), headers=self.headers)

        return r.json()

    def update(self, id: str, events: str, url: str, secret: str = None) -> dict:
        """
        Function to update a new webhook
        :param id: id of the webhook object
        :param events: This is a list of events that the webhook should be triggered for.
                       Alternative you can use a list containing a single entry of "*" to signify trigger for all events. (required)
        :param url: This is the URL to send the webhook to (required).
        :param secret: This is if you want to specify your own secret, if not a random one will be created for you (optional).
        :return: object json
        """
        payload = {'events': events, 'url': url}

        if secret:
            payload['secret'] = secret

        r = requests.put(self.url + '/{}'.format(id), headers=self.headers, params=payload)

        return r.json()

    def delete(self, id: str) -> dict:
        """
        Function to delete a new webhook
        :param id: id of the webhook object
        :return: object json
        """
        r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

        return r.json()
