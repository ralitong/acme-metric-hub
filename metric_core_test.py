import unittest
from metric_core import MetricCore


class TestMetricCore(unittest.TestCase):

    def setUp(self):
        self.metric_core = MetricCore(log_level='DEBUG')

    def test_storing_of_report(self):
        server_name = 't-111111111'
        start_time = '2021-05-17T10:12:33Z'
        end_time = '2021-05-17T11:15:33Z'
        self.metric_core.store({ 'server_name': server_name, 'start_time': start_time, 'end_time': end_time })

        self.assertEqual(self.metric_core.reports[server_name][0]['start_time'], start_time)
        self.assertEqual(self.metric_core.reports[server_name][0]['end_time'], end_time)

    def test_storing_more_than_one_report_same_server(self):
        server_name = 't-222222222'
        one = { 'server_name': server_name, 'start_time': '2021-05-17T11:12:33Z', 'end_time': '2021-05-17T12:15:33Z' }
        two = { 'server_name': server_name, 'start_time': '2021-05-17T12:12:33Z', 'end_time': '2021-05-17T13:15:33Z' }

        self.metric_core.store(one)
        self.metric_core.store(two)
        data = self.metric_core.reports[server_name]
        self.assertEqual(len(data), 2)

    def test_storing_more_than_one_report_data_different_server(self):
        server_one = 't-222222222'
        server_one_data_one = { 'server_name': server_one, 'start_time': '2021-05-17T11:12:33Z', 'end_time': '2021-05-17T12:15:33Z' }
        server_one_data_two = { 'server_name': server_one, 'start_time': '2021-05-17T12:12:33Z', 'end_time': '2021-05-17T13:15:33Z'
        }

        server_two = 't-333333333'
        server_two_data_one = { 'server_name': server_two, 'start_time': '2021-05-17T13:12:33Z', 'end_time': '2021-05-17T14:15:33Z' }

        self.metric_core.store(server_one_data_one)
        self.metric_core.store(server_one_data_two)
        self.metric_core.store(server_two_data_one)

        server_one_data = self.metric_core.reports[server_one]
        server_two_data = self.metric_core.reports[server_two]
        self.assertEqual(len(server_one_data), 2)
        self.assertEqual(len(server_two_data), 1)

    def test_computing_of_report_time_gap_in_seconds(self):
        seconds = self.metric_core.compute_gap({ 'start_time': '2021-11-04T14:49:43.766733', 'end_time': '2021-11-04T15:24:37.766733' })
        self.assertEqual(seconds, 2094)

    def test_computing_of_mean_of_durations(self):
        durations = [ 
            { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
            { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
            { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
        ]

        mean = self.metric_core.compute_mean(durations)
        self.assertEqual(mean, 1751)

    def test_computing_of_standard_deviation_of_durations(self):
        durations = [
            { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
            { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
            { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
        ]

        standard_deviation = self.metric_core.compute_standard_deviation(
            durations)
        self.assertEqual(standard_deviation, 75)

    def test_extracting_duration_from_reports(self):
        reports = {
            't-111111111': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
            ],
            't-222222222': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' }
            ]
        }

        self.metric_core.reports = reports

        actual = self.metric_core.get_all_durations()

        expected = [ 
            { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
            { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
            { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' },
            { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' }
        ]

        self.assertListEqual(actual, expected)

    def test_getting_overall_mean(self):
        reports = {
            't-111111111': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
            ],
            't-222222222': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
            ],
            't-222222222': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
            ]
        }

        self.metric_core.reports = reports
        mean = self.metric_core.get_overall_mean()
        self.assertEqual(mean, 1751)

    def test_getting_overall_standard_deviation(self):
        inputs = {
            't-111111111': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
            ],
            't-222222222': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
            ],
            't-333333333': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
            ]
        }

        self.metric_core.reports = inputs
        standard_deviation = self.metric_core.get_overall_standard_deviation()
        self.assertEqual(standard_deviation, 65)

    def test_processing_outliers(self):
        inputs = {
            't-111111111': [
                { 'start_time': '2021-11-05T16:50:12.490015', 'end_time': '2021-11-05T17:18:22.490015' },
                { 'start_time': '2021-11-05T16:50:12.490015', 'end_time': '2021-11-05T17:18:22.490015' },
                { 'start_time': '2021-11-05T16:50:12.490668', 'end_time': '2021-11-05T17:19:14.490668' }
            ],
            't-222222222': [
                { 'start_time': '2021-11-05T16:50:12.491387', 'end_time': '2021-11-05T17:19:49.491387' },
                { 'start_time': '2021-11-05T16:50:12.495193', 'end_time': '2021-11-05T17:18:59.495193' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
            ],
            't-333333333': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:23:09.285827' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
            ],
            't-444444444': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:23:09.285827' },
                # the outlier
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:43:45.295629' }
            ]
        }

        self.metric_core.reports = inputs

        outliers = self.metric_core.get_outlier_servers()
        expected = [ 't-444444444' ]
        self.assertListEqual(expected, outliers)


    def test_process_statistics(self):
        inputs = {
            't-111111111': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
            ],
            't-222222222': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
            ],
            't-333333333': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
            ]
        }

        self.metric_core.reports = inputs

        processed_statistics = self.metric_core.process_statistics()
        self.assertEqual(processed_statistics['mean'], 1754)
        self.assertEqual(processed_statistics['stddev'], 62)

    def test_process_statistics_should_return_empty_object_when_less_than_ten_durations(self):
        inputs = {
            't-111111111': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
            ],
            't-222222222': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' }
            ],
            't-333333333': [
                { 'start_time': '2021-11-04T15:49:03.224052', 'end_time': '2021-11-04T16:16:48.224052' },
                { 'start_time': '2021-11-04T15:49:03.285827', 'end_time': '2021-11-04T16:19:09.285827' },
                { 'start_time': '2021-11-04T15:49:03.295629', 'end_time': '2021-11-04T16:18:45.295629' },
            ]
        }

        self.metric_core.reports = inputs

        processed_statistics = self.metric_core.process_statistics()
        self.assertEqual(processed_statistics['mean'], '')
        self.assertEqual(processed_statistics['stddev'], '')

if __name__ == '__main__':
    unittest.main()
