""" Unittests for civo.py
"""
from unittest import main, TestCase
from unittest.mock import patch, call

from civo import Civo


class TestCivo(TestCase):

    def test_construct_no_api_key(self):
        """ Test Civo Constructor
        """
        with self.assertRaises(Exception):
            civo = Civo()

    @patch('os.getenv')
    def test_construct_api_key_env(self, m_getenv):
        """ Test Civo Constructor
        """
        m_getenv.return_value = 'FOO'
        civo = Civo()
        self.assertEqual(civo.token, 'FOO')
        m_getenv.assert_has_calls([call('CIVO_TOKEN', False)])

    @patch('os.getenv')
    def test_construct_api_key_argv(self, m_getenv):
        """ Test Civo Constructor
        """
        m_getenv.return_value = ''
        civo = Civo(civo_token='BAR')
        self.assertEqual(civo.token, 'BAR')
        self.assertTrue(('CIVO_TOKEN', False) not in m_getenv.call_args_list)

    @patch('os.getenv')
    def test_construct_api_key_env_and_argv(self, m_getenv):
        """ Test Civo Constructor
        """
        m_getenv.return_value = 'FOO'
        civo = Civo(civo_token='BAR')
        self.assertEqual(civo.token, 'BAR')
        self.assertTrue(('CIVO_TOKEN', False) not in m_getenv.call_args_list)


if __name__ == '__main__':
    main()
