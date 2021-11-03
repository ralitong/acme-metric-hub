from datetime import datetime
import unittest
import time
from acme_server import AcmeServer

class TestAcmeServer(unittest.TestCase):

    def setUp(self):
        self.acme_server = AcmeServer()
        
    def test_generate_utc_date(self):
        date = self.acme_server.generate_utc_date()
        self.assertIsNotNone(date)

    def test_generate_server_name(self):
        name = self.acme_server.generate_server_name()
        self.assertIsNotNone(name)

    def test_server_name_should_be_present(self):
        self.assertIsNotNone(self.acme_server.name)

    def test_generate_normal_interval(self):
        interval = self.acme_server.generate_normal_interval()
        self.assertLessEqual(interval, self.acme_server.normal_interval_upper)

    def test_generate_unusual_interval(self):
        interval = self.acme_server.generate_unusual_interval()
        self.assertLessEqual(interval, self.acme_server.unusual_interval_upper)

    def test_generate_normal_time_interval(self):
        interval = self.acme_server.generate_normal_time_interval()
        self.assertIsNotNone(interval['start_time'])
        self.assertIsNotNone(interval['end_time'])

    def test_generate_normal_time_interval_gap_is_correct(self):
        interval = self.acme_server.generate_normal_time_interval()

    def test_generate_normal_batch_process(self):
        request = self.acme_server.generate_normal_batch_process()
        self.assertIsNotNone(request['server_name'])
        self.assertIsNotNone(request['start_time'])
        self.assertIsNotNone(request['end_time'])

    def test_generate_unusual_time_interval(self):
        interval = self.acme_server.generate_unusual_time_interval()
        self.assertIsNotNone(interval['start_time'])
        self.assertIsNotNone(interval['end_time'])

    def test_generate_unusual_batch_process(self):
        request = self.acme_server.generate_unusual_batch_process()
        self.assertIsNotNone(request['server_name'])
        self.assertIsNotNone(request['start_time'])
        self.assertIsNotNone(request['end_time'])

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()