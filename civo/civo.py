import os

from .dns import Dns
from .firewall import Firewall
from .intances import Instances
from .loadbalance import LoadBalance
from .networks import Networks
from .snapshots import Snapshots
from .ssh import Ssh
from .volumes import Volumes
from .webhook import WebHook


class Civo:

    def __init__(self, civo_token: str = None):
        """
        Init for Civo class
        :param civo_token: str, optional the token generate by civo
        """

        # Get token from env or pass to the class
        if not civo_token:
            self.token = os.getenv('CIVO_TOKEN', False)
        else:
            self.token = civo_token

        # Create headers for all requests to civo api
        if not self.token:
            raise Exception('CIVO_TOKEN not found in the enviroment or is not declared in the class')

        self.headers = {'Authorization': 'bearer {}'.format(self.token)}

        # Ssh class
        self.ssh = Ssh(self.headers)
        self.instances = Instances(self.headers)
        self.networks = Networks(self.headers)
        self.snapshots = Snapshots(self.headers)
        self.volumes = Volumes(self.headers)
        self.firewalls = Firewall(self.headers)
        self.dns = Dns(self.headers)
        self.loadbalance = LoadBalance(self.headers)
        self.webhook = WebHook(self.headers)