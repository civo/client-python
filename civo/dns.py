import requests

from .utils import filter_list


class Dns:
    """
    We host reverse DNS for all instances automatically. If you'd like to manage forward (normal)
    DNS for your domains, you can do that for free within your account. This API is effectively split
    in to two parts: 1) Managing domain names themselves, and 2) Managing records within those domain names.
    We don't offer registration of domains names, this is purely for hosting the DNS.
    If you're looking to buy a domain name, we recommend LCN.com for their excellent friendly support
    and very competitive prices.
    """

    def __init__(self, headers, api_url):
        self.headers = headers
        self.url = '{}/v2/dns'.format(api_url)

    def create(self, name: str) -> dict:
        """
        Function to setup a new domain
        :param name: the domain name, e.g. "example.com"
        :return: object json
        """
        payload = {'name': name}
        r = requests.post(self.url, headers=self.headers, params=payload)

        return r.json()

    def update(self, id: str, name: str) -> dict:
        """
        Function to update a new domain
        :param name: the domain name, e.g. "example.com"
        :return: object json
        """
        payload = {'name': name}
        r = requests.put(self.url + '/{}'.format(id), headers=self.headers, params=payload)

        return r.json()

    def search(self, filter: str = None) -> dict:
        """
        Function to list all dns domains
        :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                       you can filter by any object that is inside the json
        :return: object json
        """
        r = requests.get(self.url, headers=self.headers)

        if filter:
            data = r.json()
            return filter_list(data=data, filter_by=filter)

        return r.json()

    def delete(self, id: str) -> dict:
        """
        Function to deleting a domain
        :param id: id of the domain object
        :return: object json
        """
        r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

        return r.json()

    def create_record(self, id: str, type: str, name: str, value: str, priority: str, ttl: str = '600') -> dict:
        """
        Function to create a new DNS record
        :param id: id of the domain object
        :param type: the choice of RR type from (a, cname, mx or txt)
        :param name: the portion before the domain name (e.g. www) or an @ for the apex/root domain
                     (you cannot use an A record with an amex/root domain)
        :param value: the IP address (A or MX), hostname (CNAME or MX) or text value (TXT) to serve for this record
        :param priority: useful for MX records only, the priority mail should be attempted it (defaults to 10)
        :param ttl: how long caching DNS servers should cache this record for, in seconds
                    (the minimum is 600 and the default if unspecified is 600)
        :return: object json
        """
        payload = {'type': type, 'name': name, 'value': value, 'priority': priority, 'ttl': ttl}
        r = requests.post(self.url + '{}/records'.format(id), headers=self.headers, params=payload)

        return r.json()

    def update_record(self, id: str, id_record: str, type: str = None, name: str = None, value: str = None,
                      priority: str = None,
                      ttl: str = None) -> dict:
        """
        Function to update a DNS record
        :param id: id of the domain object
        :param id_record: id of the record domain object
        :param type: the choice of RR type from (a, cname, mx or txt)
        :param name: the portion before the domain name (e.g. www) or an @ for the apex/root domain
                     (you cannot use an A record with an amex/root domain)
        :param value: the IP address (A or MX), hostname (CNAME or MX) or text value (TXT) to serve for this record
        :param priority: useful for MX records only, the priority mail should be attempted it (defaults to 10)
        :param ttl: how long caching DNS servers should cache this record for, in seconds
                    (the minimum is 600 and the default if unspecified is 600)
        :return: object json
        """
        payload = {}

        if type:
            payload['type'] = type

        if name:
            payload['name'] = name

        if value:
            payload['value'] = value

        if priority:
            payload['priority'] = priority

        if ttl:
            payload['ttl'] = ttl

        r = requests.put(self.url + '{}/records/{}'.format(id, id_record), headers=self.headers, params=payload)

        return r.json()

    def lists_record(self, id: str, filter: str = None) -> dict:
        """
        Function to list DNS records
        :param id: Firewall object id
        :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                       you can filter by any object that is inside the json
        :return: object json
        """
        r = requests.get(self.url + '{}/records'.format(id), headers=self.headers)

        if filter:
            data = r.json()
            return filter_list(data=data, filter_by=filter)

        return r.json()

    def delete_record(self, id: str, record_id: str) -> dict:
        """
        Function to deleting a dns record
        :param id: id of the dns object
        :param record_id: id of the dns record object
        :return: object json
        """
        r = requests.delete(self.url + '/{}/records/{}'.format(id, record_id), headers=self.headers)

        return r.json()
