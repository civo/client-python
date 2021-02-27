import os

from .charges import Charges
from .dns import Dns
from .firewall import Firewall
from .intances import Instances
from .kubernetes import Kubernetes
from .loadbalance import LoadBalance
from .networks import Networks
from .quota import Quota
from .regions import Regions
from .size import Size
from .snapshots import Snapshots
from .ssh import Ssh
from .templates import Templates
from .volumes import Volumes
from .webhook import WebHook
from .utils import print_err


class Civo:

    def __init__(self, civo_token: str = None, api_url: str = None, region: str = None):
        """
        Init for Civo class
        :param civo_token: str, optional the token generate by civo
        """

        # Get token from env or pass to the class
        if not civo_token:
            self.token = os.getenv('CIVO_TOKEN', False)
        else:
            self.token = civo_token

        # Get api url from env or you can pass to the class
        if not api_url:
            self.api_url = os.getenv('CIVO_API', 'https://api.civo.com')

        if not region:
            print_err('Using Default Region')
            self.region = None
        else:
            self.region = region

        # Create headers for all requests to civo api
        if not self.token:
            raise Exception('CIVO_TOKEN not found in the environment or is not declared in the class')

        self.headers = {'Authorization': 'bearer {}'.format(self.token)}

        # int all class
        self.ssh = Ssh(self.headers, self.api_url)
        self.instances = Instances(self.headers, self.api_url, self.region)
        self.networks = Networks(self.headers, self.api_url, self.region)
        self.snapshots = Snapshots(self.headers, self.api_url, self.region)
        self.volumes = Volumes(self.headers, self.api_url, self.region)
        self.firewalls = Firewall(self.headers, self.api_url, self.region)
        self.dns = Dns(self.headers, self.api_url)
        self.loadbalance = LoadBalance(self.headers, self.api_url, self.region)
        self.webhook = WebHook(self.headers, self.api_url)
        self.size = Size(self.headers, self.api_url)
        self.regions = Regions(self.headers, self.api_url)
        self.templates = Templates(self.headers, self.api_url)
        self.quota = Quota(self.headers, self.api_url)
        self.charges = Charges(self.headers, self.api_url)
        self.kubernetes = Kubernetes(self.headers, self.api_url, self.region)
