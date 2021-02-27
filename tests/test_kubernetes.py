""" Test Kubernetes API
"""
from unittest import main
from tests import TestingBase, wait_until


class TestKubernetes(TestingBase):

    def test_kubernetes(self):
        """ Test all operations on a cluster
        Create, Retrieve, Update then Delete a Cluster
        """
        name = "test_create_k8s"
        region = 'NYC1'
        nodes = 1
        size = "g3.xsmall"

        cluster = self.civo.kubernetes.create(name=name, region=region, nodes_size=size, num_nodes=nodes)
        if 'code' in cluster.keys():
            self.fail('Error in Create Response: %s\n%s' % (cluster['code'], cluster['reason']))

        self.assertEqual(cluster['name'], name)
        _id = cluster['id']

        f_status = lambda: self.civo.kubernetes.retrieving(_id, region=region)['ready']
        wait_until(f_status, 480, 120, "Wait until cluster ready")

        result = self.civo.kubernetes.update(id=_id, num_nodes=2, region=region)
        wait_until(f_status, 480, 120, "Wait until cluster updated")

        result = self.civo.kubernetes.delete(id=_id, region=region)
        self.assertEqual(result["result"], "success")

    def test_kubernetes_list_retrieve(self):
        """ Test Perform List and Retrieve of Cluster
        """
        results = self.civo.kubernetes.search()
        self.assertGreater(len(results['items']), 0)
        _id = results['items'][0]['id']
        self.assertIsInstance(results['items'][0]['name'], str)

        details = self.civo.kubernetes.retrieving(_id)
        self.assertTrue(details)

    def test_kubernetes_marketplace(self):
        """
        Test query kubernetes marketplace
        """
        data = self.civo.kubernetes.marketplace()
        self.assertTrue(data)

    def test_kubernetes_versions(self):
        """
        Test query kubernetes versions
        """
        data = self.civo.kubernetes.versions()
        self.assertTrue(data)


if __name__ == '__main__':
    main()
