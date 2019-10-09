import unittest

from civo import Civo

civo = Civo(civo_token='dDq7uUCrk30jVBwX2f41FeWAvyM0Y8iS5OaNzIgJGlHcEPs9mR')


class TestSsh(unittest.TestCase):

    def test_ssh_create(self):
        """
        Test if can create ssh key
        """
        result = civo.ssh.create(name='test_ssh', public_key='test_public_key')

        self.assertEqual(result['result'], 'success')

    def test_ssh_list(self):
        """
        Test to list all ssh key
        """
        result = civo.ssh.lists(filter='name:test_ssh')

        self.assertEqual(result[0]['name'], 'test_ssh')

    def test_ssh_retrieving(self):
        """
        Test to retrieving ssh key
        """
        id = civo.ssh.search(filter='name:test_ssh')[0]['id']
        result = civo.ssh.retrieving(id=id)

        self.assertEqual(result['name'], 'test_ssh')

    def test_ssh_update(self):
        """
        Test to update ssh key
        """
        id = civo.ssh.search(filter='name:test_ssh')[0]['id']
        result = civo.ssh.updating(id=id, name='new_test_ssh')

        self.assertEqual(result['name'], 'new_test_ssh')

    def test_ssh_z_delete(self):
        """
        Test to delete ssh key
        """
        id = civo.ssh.search(filter='name:new_test_ssh')[0]['id']
        result = civo.ssh.delete(id=id)

        self.assertEqual(result['result'], 'success')


class TestInstances(unittest.TestCase):

    def test_instances_create(self):
        """
        Test if can create instances
        """
        size = civo.size.search(filter='name:g2.xsmall')[0]['name']
        template = civo.templates.search(filter='code:debian-stretch')[0]['id']

        result = civo.instances.create(hostname='test-instance.com', size=size,
                                       template_id=template,
                                       ssh_key_id='default')

        self.assertEqual(result['status'], 'BUILD_PENDING')

    def test_instances_list(self):
        """
        Test to list all instances
        """
        result = civo.instances.search(filter='hostname:test-instance.com')

        self.assertEqual(result[0]['hostname'], 'test-instance.com')
    #
    # def test_instances_retrieving(self):
    #     """
    #     Test to retrieving ssh key
    #     """
    #     id = civo.ssh.search(filter='name:test_ssh')[0]['id']
    #     result = civo.ssh.retrieving(id=id)
    #
    #     self.assertEqual(result['name'], 'test_ssh')
    #
    # def test_instances_update(self):
    #     """
    #     Test to update ssh key
    #     """
    #     id = civo.ssh.search(filter='name:test_ssh')[0]['id']
    #     result = civo.ssh.updating(id=id, name='new_test_ssh')
    #
    #     self.assertEqual(result['name'], 'new_test_ssh')
    #
    # def test_instances_z_delete(self):
    #     """
    #     Test to delete ssh key
    #     """
    #     id = civo.ssh.search(filter='name:new_test_ssh')[0]['id']
    #     result = civo.ssh.delete(id=id)
    #
    #     self.assertEqual(result['result'], 'success')

if __name__ == '__main__':
    unittest.main()
