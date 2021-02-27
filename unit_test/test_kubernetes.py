""" Unittests for kubernetes.py
"""
from json import loads
from unittest import main
from unittest.mock import patch
from unit_test import TestingBase

from civo import Civo


FAKE_TOKEN = "foobar"


class TestKubernetes(TestingBase):
    url = "https://api.civo.com/v2/kubernetes/clusters"

    @patch('requests.get')
    @patch('requests.post')
    def test_create_cluster_default_region(self, m_post, m_get):
        """ Test Create Cluster
        """
        resp, data, status = self.get_response('create_clusters.json')
        m_post.return_value = resp

        net_resp, net_data, net_status = self.get_response('get_network.json')
        m_get.return_value = net_resp

        self.add_auth()
        self.add_defaults()

        civo = Civo(civo_token=self.api_key)
        _out = civo.kubernetes.create(name="SomeCluster")

        self.assertIsNone(civo.region)
        m_post.assert_called_once_with(self.url, headers=self.headers, params=self.params)
        self.assertDictEqual(_out, loads(data))

    @patch('requests.post')
    def test_create_cluster_region_in_construct(self, m_post):
        """ Test Create Cluster
        """
        resp, data, status = self.get_response('create_clusters.json')
        m_post.return_value = resp

        self.add_auth()
        self.add_defaults()

        civo = Civo(civo_token=self.api_key, region="NYC1")
        _out = civo.kubernetes.create(name="SomeCluster")

        m_post.assert_called_once_with(self.url + "?region=NYC1", headers=self.headers, params=self.params)
        self.assertEqual(_out, data)

    @patch('requests.post')
    def test_create_cluster_region_in_create(self, m_post):
        """ Test Create Cluster
        """
        resp, data, status = self.get_response('create_clusters.json')
        m_post.return_value = resp

        self.add_auth()
        self.add_defaults()

        civo = Civo(civo_token=self.api_key)
        _out = civo.kubernetes.create(name="SomeCluster", region="NYC1")

        m_post.assert_called_once_with(self.url + "?region=NYC1", headers=self.headers, params=self.params)
        self.assertEqual(_out, data)

    @patch('requests.post')
    def test_create_cluster_region_in_base_and_create(self, m_post):
        """ Test Create Cluster
        """
        resp, data, status = self.get_response('create_clusters.json')
        m_post.return_value = resp

        self.add_auth()
        self.add_defaults()

        civo = Civo(civo_token=self.api_key, region="XYZ")
        _out = civo.kubernetes.create(name="SomeCluster", region="NYC1")

        m_post.assert_called_once_with(self.url + "?region=NYC1", headers=self.headers, params=self.params)
        self.assertEqual(_out, data)

    @patch('requests.get')
    def test_search(self, m_get):
        """ Test Cluster Search
        """
        pass

    @patch('requests.get')
    def test_retrieving(self, m_get):
        """ Test Get Cluster Detail
        """
        pass

    @patch('requests.put')
    def test_update(self, m_put):
        """ Test Update Cluster
        """

    @patch('requests.get')
    def test_marketplace(self, m_get):
        """ Test List Marketplace
        """
        pass

    @patch('requests.delete')
    def test_delete(self, m_del):
        """ Test Delete Cluster
        """
        pass

    @patch('requests.post')
    def test_recycle(self, m_get):
        """ Test Recycle Cluster Node
        """
        pass

    @patch('requests.get')
    def test_versions(self, m_get):
        """ Test for endpoint: kubernetes/versions
        """
        pass


if __name__ == '__main__':
    main()
