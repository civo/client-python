import requests

from .exceptions import CIVOAPIError
from .networks import Networks
from .utils import filter_list


class Kubernetes:
    """
    Kubernetes clusters are a number of instances on the Civo cloud platform running the Kubernetes cloud orchestration platform.
    """
    supported_k8s = ['NYC1', 'SVG1']

    def __init__(self, headers, api_url, region=None):
        self.region = region
        self.headers = headers
        self._api_url = api_url
        self.url = '{}/v2/kubernetes/clusters'.format(self._api_url)
        self.kube_version = '{}/v2/kubernetes/versions'.format(self._api_url)
        self.marketplace_url = '{}/v2/kubernetes/applications'.format(self._api_url)

    def get_url(self, path=None, region=None):
        """ Construct the API URL, appending necessary parameters
        :param path: additional path components (optional)
        :param region: target region (optional)
        :return: str
        """
        region = region if region else self.region

        if region is not None and region not in self.supported_k8s:
            raise CIVOAPIError('Kubernetes is not supported in: %s' % region)
        path = path if path else ""
        query = "?region={region}".format(region=region) if region else ""
        return self.url + path + query

    def create(self, name: str, num_nodes: int = 3, nodes_size: str = 'g3.small', kubernetes_version: str = None,
               tags: str = None, network: str = None, region: str = None) -> dict:
        """
        Function to create a cluster of kubernetes
        :param name: a name for your cluster, must be unique within your account (required)
        :param num_nodes: the number of instances to create (optional, the default at the time of writing is 3)
        :param nodes_size: the size of each node (optional, the default is currently g2.small)
        :param kubernetes_version: the version of k3s to install (optional, the default is currently the latest available)
        :param tags: a space separated list of tags, to be used freely as required (optional)
        :param network: network to be attached to cluster instance, not validated (optional, default: Default)
        :param region: the civo region to be used for instance creation, not validated (optional)
        :return: dict
        """
        payload = {
            'name': name,
            'num_target_nodes': num_nodes,
            'target_nodes_size': nodes_size,
            'tags': '',
            'applications': '',
            'kubernetes_version': ''
        }

        if tags:
            payload['tags'] = tags

        if kubernetes_version:
            payload['kubernetes_version'] = kubernetes_version

        networks_list = Networks(self.headers, self._api_url, region).search()
        if not network:
            payload['network_id'] = [i['id'] for i in networks_list if i['default']][0]
        else:
            payload['network_id'] = [i['id'] for i in networks_list if i['name'] == network or i['id'] == network][0]

        r = requests.post(self.get_url(region=region), headers=self.headers, params=payload)

        return r.json()

    def search(self, filter: str = None, region: str = None) -> dict:
        """
        A list of clusters accessible from an account is available
        :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
           you can filter by any object that is inside the json
        :param region: the civo region to be used for instance creation, not validated (optional)
        :return: objects dict
        """
        payload = {}

        r = requests.get(self.get_url(region=region), headers=self.headers, params=payload)

        if filter:
            data = r.json()
            return filter_list(data=data, filter_by=filter)

        return r.json()

    def retrieving(self, id: str, region: str = None) -> object:
        """
        Function to retrieving a single cluster's details
        :param id: id of the objects
        :param region: the civo region to be used for instance creation, not validated (optional)
        :return: object json
        """
        r = requests.get(self.get_url(region=region, path='/{}'.format(id)), headers=self.headers)

        return r.json()

    def update(self, id: str, name: str = None, num_nodes: int = None, applications: str = None, version: str = None,
               node_destroy: str = None, region: str = None) -> dict:
        """
        Function to update a cluster of kubernetes
        :param node_destroy: if you are scaling down by one, you can give a hint on the node's name to be destroyed.
        :param version: the version of k3s to upgrade to.
        :param applications: a comma separated list of applications to install. Spaces within application names are fine
               but shouldn't be either side of the comma.
        :param id: id of the cluster
        :param name: the cluster's new name
        :param num_nodes: how many nodes should the cluster scale to.
        :param region: the civo region to be used for instance creation, not validated (optional)
        :return: dict
        """
        payload = {}

        if name:
            payload['name'] = name

        if num_nodes:
            payload['num_target_nodes'] = num_nodes

        if version:
            payload['version'] = version

        if node_destroy:
            payload['node_destroy'] = node_destroy

        if applications:
            payload['applications'] = applications

        r = requests.put(self.get_url(region=region, path='/{}'.format(id)), headers=self.headers, params=payload)

        return r.json()

    def marketplace(self, filter: str = None) -> dict:
        """
        A user can install applications in to their cluster from the marketplace using the `update` call above.
        :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
           you can filter by any object that is inside the json
        :return: objects dict
        """
        payload = {}

        r = requests.get(self.marketplace_url, headers=self.headers, params=payload)

        if filter:
            data = r.json()
            return filter_list(data=data, filter_by=filter)

        return r.json()

    def delete(self, id: str, region: str = None) -> dict:
        """
        A user can delete a cluster and all underlying nodes.
        :param id: id of the cluster
        :param region: the civo region to be used for instance creation, not validated (optional)
        :return: dict
        """

        r = requests.delete(self.get_url(region=region, path='/{}'.format(id)), headers=self.headers)

        return r.json()

    def recycle(self, id: str, hostname: str, region: str = None) -> dict:
        """
        A user can delete and recreate one of the underlying nodes, if it's having a problem.
        :param hostname: he name of the node to recycle.
        :param id: id of the cluster
        :param region: the civo region to be used for instance creation, not validated (optional)
        :return: dict
        """
        payload = {'hostname': hostname}

        r = requests.post(self.get_url(region=region, path='/{}/recycle'.format(id)), headers=self.headers, payload=payload)

        return r.json()

    def versions(self, filter: str = None) -> dict:
        """
        A list of versions available to install isavailable
        :param filter: Filter json object the format is 'type:stable',
           you can filter by any object that is inside the json
        :return: objects dict
        """
        payload = {}

        r = requests.get(self.kube_version, headers=self.headers, params=payload)

        if filter:
            data = r.json()
            return filter_list(data=data, filter_by=filter)

        return r.json()
