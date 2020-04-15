import requests

from .utils import filter_list


class Kubernetes:
    """
    Kubernetes clusters are a number of instances on the Civo cloud platform running the Kubernetes cloud orchestration platform.
    """

    def __init__(self, headers, api_url):
        self.headers = headers
        self.url = 'https://{}/v2/kubernetes/clusters'.format(api_url)
        self.kube_version = 'https://{}/v2/kubernetes/versions'.format(api_url)
        self.marketplace_url = 'https://{}/v2/kubernetes/applications'.format(api_url)

    def create(self, name: str, num_nodes: int = 3, nodes_size: str = 'g2.small', kubernetes_version: str = None,
               tags: str = None) -> dict:
        """
        Function to create a cluster of kubernetes
        :param name: a name for your cluster, must be unique within your account (required)
        :param num_nodes: the number of instances to create (optional, the default at the time of writing is 3)
        :param nodes_size: the size of each node (optional, the default is currently g2.small)
        :param kubernetes_version: the version of k3s to install (optional, the default is currently the latest available)
        :param tags: a space separated list of tags, to be used freely as required (optional)
        :return: dict
        """
        payload = {'name': name, 'num_target_nodes': num_nodes, 'target_nodes_size': nodes_size}

        if tags:
            payload['tags'] = tags

        if kubernetes_version:
            payload['kubernetes_version'] = kubernetes_version

        r = requests.post(self.url, headers=self.headers, params=payload)

        return r.json()

    def search(self, filter: str = None) -> dict:
        """
        A list of clusters accessible from an account is available
        :param filter: Filter json object the format is 'id:6224cd2b-d416-4e92-bdbb-db60521c8eb9',
           you can filter by any object that is inside the json
        :return: objects dict
        """
        payload = {}

        r = requests.get(self.url, headers=self.headers, params=payload)

        if filter:
            data = r.json()
            return filter_list(data=data, filter=filter)

        return r.json()

    def retrieving(self, id: str) -> object:
        """
        Function to retrieving a single cluster's details
        :param id: id of the objects
        :return: object json
        """
        r = requests.get(self.url + '/{}'.format(id), headers=self.headers)

        return r.json()

    def update(self, id: str, name: str = None, num_nodes: int = None, applications: str = None, version: str = None,
               node_destroy: str = None) -> dict:
        """
        Function to update a cluster of kubernetes
        :param node_destroy: if you are scaling down by one, you can give a hint on the node's name to be destroyed.
        :param version: the version of k3s to upgrade to.
        :param applications: a comma separated list of applications to install. Spaces within application names are fine
               but shouldn't be either side of the comma.
        :param id: id of the cluster
        :param name: the cluster's new name
        :param num_nodes: how many nodes should the cluster scale to.
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

        r = requests.put(self.url + '/{}'.format(id), headers=self.headers, params=payload)

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
            return filter_list(data=data, filter=filter)

        return r.json()

    def delete(self, id: str) -> dict:
        """
        A user can delete a cluster and all underlying nodes.
        :param id: id of the cluster
        :return: dict
        """

        r = requests.delete(self.url + '/{}'.format(id), headers=self.headers)

        return r.json()

    def recycle(self, id: str, hostname: str) -> dict:
        """
        A user can delete and recreate one of the underlying nodes, if it's having a problem.
        :param hostname: he name of the node to recycle.
        :param id: id of the cluster
        :return: dict
        """
        payload = {'hostname': hostname}

        r = requests.post(self.url + '/{}/recycle'.format(id), headers=self.headers, payload=payload)

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
            return filter_list(data=data, filter=filter)

        return r.json()
