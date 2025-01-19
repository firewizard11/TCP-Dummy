import socket
import unittest
from tcp_dummy.tcp_client import TCPClient

class TCPClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = TCPClient()

    def test_client_creation(self):
        self.assertEqual(self.client.timeout, 5)
        self.assertEqual(self.client.current_connection, None)

    def test_client_getters(self):
        self.assertEqual(self.client.get_timeout(), 5)

    def test_client_setters(self):
        self.client.set_timeout(10)

        self.assertEqual(self.client.timeout, 10)