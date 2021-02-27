import requests

from .utils import filter_list


class Firewall:
    """
    The simplest solution for most customers is to configure a firewall within their
    Instances using either iptables which is powerful or Uncomplicated Firewall/ufw
    which is much simpler but only works on Ubuntu.

    As an another option, customers can configure custom firewall rules for their
    instances using the Firewall API which adjusts the security group for your network
    of instances. These are a freely configurable option, however customers
    should be careful to not lock out their access to the instances.
    """

    def __init__(self, headers, api_url, region):
        param = "?region={region}".format(region=region) if region else ''
        self.headers = headers
        self.url = '{api_url}/v2/firewalls{param}'.format(api_url=api_url, param=param)

    def create(self, name: str, region: str = None) -> dict:
        """
        Function to create a new firewall
        :param name: A unique name for this firewall within your account
        :return: object json
        """
        payload = {'name': name}
        r = requests.post(self.url, headers=self.headers, params=payload)

        return r.json()

    def search(self, filter: str = None) -> dict:
        """
        Function to list firewalls
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
        Function to deleting a firewall
        :param id: id of the firewall object
        :return: object json
        """
        r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

        return r.json()

    def create_rule(self, id: str, start_port: str, protocol: str = 'tcp', end_port: str = None,
                    cidr: str = '0.0.0.0/0',
                    direction: str = 'inbound', label: str = None) -> dict:
        """
        An account holder can create firewall rules for a specific firewall, but there is a quota'd limit
        to the number of rules that can be created, but generally this is much higher than most customers
        will require and it can be increased if required.
        :param id: Firewall id object
        :param protocol: the protocol choice from tcp, udp or icmp (the default if unspecified is tcp)
        :param start_port: the start of the port range to configure for this rule (or the single port if required)
        :param end_port: the end of the port range (this is optional, by default it will only apply to the single
               port listed in start_port)
        :param cidr: the IP address of the other end (i.e. not your instance) to affect, or a valid network CIDR
                     (defaults to being globally applied, i.e. 0.0.0.0/0)
        :param direction: will this rule affect inbound or outbound traffic (by default this is inbound)
        :param label: a string that will be the displayed name/reference for this rule (optional)
        :return: object json
        """
        payload = {'protocol': protocol, 'start_port': start_port, 'cidr': cidr, 'direction': direction}

        if end_port:
            payload['end_port'] = end_port

        if label:
            payload['label'] = label

        r = requests.post(self.url + '/{}/rules'.format(id), headers=self.headers, params=payload)

        return r.json()

    def lists_rule(self, id: str, filter: str = None) -> dict:
        """
        Function to list firewalls rules
        :param id: Firewall id object
        :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
                       you can filter by any object that is inside the json
        :return: object json
        """
        r = requests.get(self.url + '/{}/rules'.format(id), headers=self.headers)

        if filter:
            data = r.json()
            return filter_list(data=data, filter_by=filter)

        return r.json()

    def delete_rule(self, id: str, rule_id: str) -> dict:
        """
        Function to deleting a firewall rule
        :param id: id of the firewall object
        :param rule_id: id of the firewall rule object
        :return: object json
        """
        r = requests.delete(self.url + '/{}/rules/{}'.format(id, rule_id), headers=self.headers)

        return r.json()