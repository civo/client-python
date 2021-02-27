""" Integration Test Base Class
"""
from time import sleep, time
import os
from unittest import TestCase
from civo import Civo


class TestingBase(TestCase):

    def __init__(self, methodName=None):
        super().__init__(methodName)

    @classmethod
    def setUpClass(cls) -> None:
        if os.getenv('CIVO_TOKEN') is None:
            raise RuntimeError('CIVO_TOKEN not set')

    def setUp(self) -> None:
        self.civo = Civo()


def wait_until(fn, timeout, period, message):
    """
    :param fn: callable function
    :param timeout:
    :param period:
    :param message:
    :return: bool
    """
    mustend = time() + timeout
    while time() < mustend:
        if fn():
            return True
        sleep(period)
    raise TimeoutError(message)
