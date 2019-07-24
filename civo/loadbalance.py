import requests
from .utils import filter_list


class LoadBalance:
    """
    If you want to create a load balancer for your instances, to spread your web traffic
    between them then you can easily launch a managed load balancer service on Civo.
    """

    def __init__(self, headers):
        self.headers = headers
        self.url = 'https://api.civo.com/v2/loadbalancers'

    def create(self, protocol: str, backends: list, hostname: str = None, tls_certificate: str = None,
               tls_key: str = None,
               port: str = None, max_request_size: str = '20', policy: str = 'random',
               health_check_path: str = '/', fail_timeout: str = '30', max_conns: str = '10',
               ignore_invalid_backend_tls: str = 'true'):
        """
        Function to setup a new load balancer
        :param hostname: the hostname to receive traffic for, e.g. "www.example.com"
                         (optional: sets hostname to loadbalancer-uuid.civo.com if blank)
        :param protocol: either http or https. If you specify https then you must also provide the next
                         two fields, the default is "http"
        :param backends: a list of backend instances, each containing an instance_id, protocol (http or https) and port
        :param tls_certificate: if your protocol is https then you should send the TLS certificate in Base64-encoded PEM format
        :param tls_key: if your protocol is https then you should send the TLS private key in Base64-encoded PEM format
        :param port: you can listen on any port, the default is "80" to match the default protocol of "http"
                     if not you must specify it here (commonly 80 for HTTP or 443 for HTTPS)
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

        payload = {'protocol': protocol, 'backends': backends}

        if hostname:
            payload['hostname'] = hostname

        if tls_certificate:
            payload['tls_certificate'] = tls_certificate

        if tls_key:
            payload['tls_key'] = tls_key

        if port:
            payload['port'] = port

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