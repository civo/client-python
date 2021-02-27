""" Unittest Base Class
"""
import os
from json import loads
from unittest import TestCase
from unittest.mock import Mock


class TestingBase(TestCase):

    def __init__(self, methodName=None):
        super().__init__(methodName)
        self.api_key = "foo"
        self.headers = {}
        self.params = {}

    def add_auth(self):
        self.headers['Authorization'] = 'bearer foo'

    def add_defaults(self):
        self.params = {'name': 'SomeCluster',
                       'num_target_nodes': 3,
                       'target_nodes_size': 'g3.small',
                       'tags': '',
                       'applications': '',
                       'kubernetes_version': '',
                       'network_id': 'network_id'
                       }

    @staticmethod
    def get_response(filename, status=200):
        resp = Mock()
        with open(os.path.join('..', 'responses', filename), 'r') as f_obj:
            data = f_obj.read()
        resp.json.return_value = loads(data)
        resp.status_code.return_value = status
        return resp, data, status
