import datetime
import unittest
from acme_core import AcmeCore

class TestAcmeServer(unittest.TestCase):

    def setUp(self):
        self.server_name_regex = 't-\d{9}'
        self.utcregex = '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
        self.acme_core = AcmeCore(log_level='DEBUG')
        
    def test_generate_utc_date(self):
        date = self.acme_core.generate_utc_date()
        self.assertTrue(isinstance(date, datetime.date))
    def test_generate_server_name(self):
        name = self.acme_core.generate_server_name()
        self.assertRegex(name, self.server_name_regex)

    def test_server_name_should_be_present(self):
        self.assertIsNotNone(self.acme_core.name)

    def test_generate_normal_interval(self):
        interval = self.acme_core.generate_normal_interval()
        self.assertLessEqual(interval, self.acme_core.normal_interval_upper)

    def test_generate_unusual_interval(self):
        interval = self.acme_core.generate_unusual_interval()
        self.assertLessEqual(interval, self.acme_core.unusual_interval_upper)

    def test_generate_normal_time_interval(self):
        interval = self.acme_core.generate_normal_time_interval()
        self.assertRegex(interval['start_time'], self.utcregex)
        self.assertRegex(interval['end_time'], self.utcregex)

    def test_generate_normal_time_interval_gap_is_correct(self):
        interval = self.acme_core.generate_normal_time_interval()

    def test_generate_normal_report(self):
        request = self.acme_core.generate_normal_report()
        self.assertRegex(request['server_name'], self.server_name_regex)
        self.assertRegex(request['start_time'], self.utcregex)
        self.assertRegex(request['end_time'], self.utcregex)

    def test_generate_unusual_time_interval(self):
        interval = self.acme_core.generate_unusual_time_interval()
        self.assertRegex(interval['start_time'], self.utcregex)
        self.assertRegex(interval['end_time'], self.utcregex)

    def test_generate_unusual_batch_process(self):
        request = self.acme_core.generate_unusual_report()
        self.assertRegex(request['server_name'], self.server_name_regex)
        self.assertRegex(request['start_time'], self.utcregex)
        self.assertRegex(request['end_time'], self.utcregex)

    def test_acme_server_should_have_metric_server(self):
        self.assertIsNotNone(self.acme_core.metric_server)

    def test_setting_acme_server_metric_server(self):
        expected_metric_server = 'http://mysite:9090'
        self.acme_core = AcmeCore(metric_server=expected_metric_server)
        self.assertEqual(expected_metric_server, self.acme_core.metric_server)

    def test_posting_of_normal_batch_process(self):
        self.acme_core.post_normal_report()

    def test_posting_of_unusual_batch_process(self):
        self.acme_core.post_unusual_report()

    def test_setting_of_log_level(self):
        self.acme_core.set_log_level('INFO')

    def test_setting_of_log_level_in_constructor(self):
        self.acme_core = AcmeCore(log_level='INFO')

if __name__ == '__main__':
    unittest.main()