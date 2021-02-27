""" Test SSH Keys API
"""
from unittest import main
from tests import TestingBase
from civo import Civo


class TestSsh(TestingBase):

    def test_ssh_create_update_delete(self):
        """ Test Creating, Reading, Updating and Deleting an SSH Key
        """
        result = self.civo.ssh.create(name='test_ssh', public_key='test_public_key')
        self.assertEqual(result['result'], 'success')

        _id = self.civo.ssh.search(filter='name:test_ssh')[0]['id']
        result = self.civo.ssh.retrieving(id=_id)
        self.assertEqual(result['name'], 'test_ssh')

        _id = self.civo.ssh.search(filter='name:test_ssh')[0]['id']
        result = self.civo.ssh.updating(id=_id, name='new_test_ssh')
        self.assertEqual(result['name'], 'new_test_ssh')

        _id = self.civo.ssh.search(filter='name:new_test_ssh')[0]['id']
        result = self.civo.ssh.delete(id=_id)
        self.assertEqual(result['result'], 'success')

    def test_ssh_list(self):
        """
        Test to list all ssh key
        """
        result = self.civo.ssh.search()

        self.assertTrue(len(result))
        self.assertIsInstance(result[0]['name'], str)


if __name__ == '__main__':
    main()
