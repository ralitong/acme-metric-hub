import unittest
from metric_server import MetricServer

class TestMetricServer(unittest.TestCase):

    def setUp(self):
        self.metric_server = MetricServer(log_level='DEBUG')

    def test_storing_of_batch_process_data(self):
        server_name = 't-111111111'
        start_time = '2021-05-17T10:12:33Z'
        end_time = '2021-05-17T11:15:33Z'
        self.metric_server.store({
            'server_name': server_name,
            'start_time': start_time,
            'end_time': end_time,
        })

        self.assertEqual(self.metric_server.storage[server_name][0]['start_time'], start_time)
        self.assertEqual(self.metric_server.storage[server_name][0]['end_time'], end_time)


    def test_storing_more_than_one_data_same_server(self):
        server_name = 't-222222222'
        one = {
            'server_name': server_name,
            'start_time': '2021-05-17T11:12:33Z',
            'end_time': '2021-05-17T12:15:33Z'
        }
        
        two = {
            'server_name': server_name,
            'start_time': '2021-05-17T12:12:33Z',
            'end_time': '2021-05-17T13:15:33Z'
        }

        self.metric_server.store(one)
        self.metric_server.store(two)
        data = self.metric_server.storage[server_name]
        self.assertEqual(len(data), 2)

    def test_storing_more_than_one_data_different_server(self):
        server_one = 't-222222222'
        server_one_data_one = {
            'server_name': server_one,
            'start_time': '2021-05-17T11:12:33Z',
            'end_time': '2021-05-17T12:15:33Z'
        }
        
        server_one_data_two = {
            'server_name': server_one,
            'start_time': '2021-05-17T12:12:33Z',
            'end_time': '2021-05-17T13:15:33Z'
        }

        server_two = 't-333333333'
        server_two_data_one = {
            'server_name': server_two,
            'start_time': '2021-05-17T13:12:33Z',
            'end_time': '2021-05-17T14:15:33Z'
        }
        
        self.metric_server.store(server_one_data_one)
        self.metric_server.store(server_one_data_two)
        self.metric_server.store(server_two_data_one)
        
        server_one_data = self.metric_server.storage[server_one]
        server_two_data = self.metric_server.storage[server_two]
        self.assertEqual(len(server_one_data), 2)
        self.assertEqual(len(server_two_data), 1)

    def test_computing_of_time_gap_in_seconds(self):
        
        seconds = self.metric_server.compute_gap({
            'start_time': '2021-11-04T14:49:43.766733',
            'end_time': '2021-11-04T15:24:37.766733',
        })

        self.assertEqual(seconds, 2094)
    
    def test_computing_of_mean_in_timegaps(self):
        timegaps = [
            {
                'start_time': '2021-11-04T15:49:03.224052',
                'end_time': '2021-11-04T16:16:48.224052'
            },
            {
                'start_time': '2021-11-04T15:49:03.285827',
                'end_time': '2021-11-04T16:19:09.285827'
            },
            {
                'start_time': '2021-11-04T15:49:03.295629',
                'end_time': '2021-11-04T16:18:45.295629'
            }
        ]

        mean = self.metric_server.compute_mean(timegaps)
        self.assertEqual(mean, 1751)

    def test_computing_of_standard_deviation_in_timegaps(self):
        timegaps = [
            {
                'start_time': '2021-11-04T15:49:03.224052',
                'end_time': '2021-11-04T16:16:48.224052'
            },
            {
                'start_time': '2021-11-04T15:49:03.285827',
                'end_time': '2021-11-04T16:19:09.285827'
            },
            {
                'start_time': '2021-11-04T15:49:03.295629',
                'end_time': '2021-11-04T16:18:45.295629'
            }
        ]

        mean = self.metric_server.compute_standard_deviation(timegaps)
        self.assertEqual(mean, 75)




if __name__ == '__main__':
    unittest.main()