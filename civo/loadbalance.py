import requests

from .utils import filter_list


class LoadBalance:
    """
    If you want to create a load balancer for your instances, to spread your web traffic
    between them then you can easily launch a managed load balancer service on Civo.
    """

    def __init__(self, headers, api_url, region):
        param = "?region={region}".format(region=region) if region else ''
        self.headers = headers
        self.url = '{api_url}/v2/loadbalancers{param}'.format(api_url=api_url, param=param)

    def create(self, backends: list, hostname: str = None, tls_certificate: str = None,
               tls_key: str = None,
               max_request_size: int = 20, policy: str = 'random',
               health_check_path: str = '/', fail_timeout: str = '30', max_conns: str = '10',
               ignore_invalid_backend_tls: str = 'true'):
        """
        Function to setup a new load balancer
        :param hostname: the hostname to receive traffic for, e.g. "www.example.com"
                         (optional: sets hostname to loadbalancer-uuid.civo.com if blank)
        :param backends: a list of backend instances, each containing an instance_id, protocol (http or https) and port
                         ej: [{'instance_id': '8878789', 'protocol': 'https', 'port': 443}, {'instance_id': '123234234', 'protocol': 'https', 'port': 443}]
        :param tls_certificate: if your protocol is https then you should send the TLS certificate in Base64-encoded PEM format
        :param tls_key: if your protocol is https then you should send the TLS private key in Base64-encoded PEM format
        :param max_request_size: the size in megabytes of the maximum request content that will be accepted, defaults to 20
        :param policy: one of: least_conn (sends new requests to the least busy server), random (sends new requests
                       to a random backend), round_robin (sends new requests to the next backend in order),
                       ip_hash (sends requests from a given IP address to the same backend), default is "random"
        :param health_check_path: what URL should be used on the backends to determine if it's OK (2xx/3xx status), defaults to "/"
        :param fail_timeout: how long to wait in seconds before determining a backend has failed, defaults to 30
        :param max_conns: how many concurrent connections can each backend handle, defaults to 10
        :param ignore_invalid_backend_tls: should self-signed/invalid certificates be ignored from the backend servers, defaults to true
        :return: object json
        """

        payload = {}

        for number, backend in enumerate(backends):
            for value in backend:
                payload['backends[{}][{}]'.format(number, value)] = backend[value]

        if hostname:
            payload['hostname'] = hostname

        if tls_certificate:
            payload['tls_certificate'] = tls_certificate

        if tls_key:
            payload['tls_key'] = tls_key

        if max_request_size:
            payload['max_request_size'] = max_request_size

        if policy:
            payload['policy'] = policy

        if health_check_path:
            payload['health_check_path'] = health_check_path

        if fail_timeout:
            payload['fail_timeout'] = fail_timeout

        if max_conns:
            payload['max_conns'] = max_conns

        if ignore_invalid_backend_tls:
            payload['ignore_invalid_backend_tls'] = ignore_invalid_backend_tls

        r = requests.post(self.url, headers=self.headers, data=payload)

        return r.json()

    def update(self, id: str, backends: list, hostname: str = None, tls_certificate: str = None,
               tls_key: str = None,
               max_request_size: int = 20, policy: str = 'random',
               health_check_path: str = '/', fail_timeout: str = '30', max_conns: str = '10',
               ignore_invalid_backend_tls: str = 'true'):
        """
        Function to setup a new load balancer
        :param hostname: the hostname to receive traffic for, e.g. "www.example.com"
                         (optional: sets hostname to loadbalancer-uuid.civo.com if blank)
        :param backends: a list of backend instances, each containing an instance_id, protocol (http or https) and port
                         ej: [{'instance_id': '8878789', 'protocol': 'https', 'port': 443}, {'instance_id': '123234234', 'protocol': 'https', 'port': 443}]
        :param tls_certificate: if your protocol is https then you should send the TLS certificate in Base64-encoded PEM format
        :param tls_key: if your protocol is https then you should send the TLS private key in Base64-encoded PEM format
        :param max_request_size: the size in megabytes of the maximum request content that will be accepted, defaults to 20
        :param policy: one of: least_conn (sends new requests to the least busy server), random (sends new requests
                       to a random backend), round_robin (sends new requests to the next backend in order),
                       ip_hash (sends requests from a given IP address to the same backend), default is "random"
        :param health_check_path: what URL should be used on the backends to determine if it's OK (2xx/3xx status), defaults to "/"
        :param fail_timeout: how long to wait in seconds before determining a backend has failed, defaults to 30
        :param max_conns: how many concurrent connections can each backend handle, defaults to 10
        :param ignore_invalid_backend_tls: should self-signed/invalid certificates be ignored from the backend servers, defaults to true
        :return: object json
        """

        payload = {}

        for number, backend in enumerate(backends):
            for value in backend:
                payload['backends[{}][{}]'.format(number, value)] = backend[value]

        if hostname:
            payload['hostname'] = hostname

        if tls_certificate:
            payload['tls_certificate'] = tls_certificate

        if tls_key:
            payload['tls_key'] = tls_key

        if max_request_size:
            payload['max_request_size'] = max_request_size

        if policy:
            payload['policy'] = policy

        if health_check_path:
            payload['health_check_path'] = health_check_path

        if fail_timeout:
            payload['fail_timeout'] = fail_timeout

        if max_conns:
            payload['max_conns'] = max_conns

        if ignore_invalid_backend_tls:
            payload['ignore_invalid_backend_tls'] = ignore_invalid_backend_tls

        r = requests.put(self.url + '/{}'.format(id), headers=self.headers, data=payload)

        return r.json()

    def search(self, filter: str = None) -> dict:
        """
        Function to list load balancers
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
        Function to deleting a load balancer
        :param id: ID of the load balancer to delete
        :return: object json
        """
        r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

        return r.json()
