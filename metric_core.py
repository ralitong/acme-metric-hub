import logging
import statistics
from dateutil import parser


class MetricCore:

    def __init__(self, log_level='INFO'):
        self.set_log_level(log_level)

    def set_log_level(self, log_level):
        level = {}
        if(log_level == 'DEBUG'):
            level = logging.DEBUG
        elif(log_level == 'INFO'):
            level = logging.INFO
        elif(log_level == 'WARNING'):
            level = logging.WARNING
        elif (log_level == 'ERROR'):
            level = logging.ERROR
        else:
            level = logging.CRITICAL
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=level)

        self.reports = {}

    def store(self, data):
        if not data['server_name'] in self.reports:
            self.reports[data['server_name']] = []

        logging.debug('Storing data: Server name={} Start date={} End date={}'.format(
            data['server_name'], data['start_time'], data['end_time']))

        self.reports[data['server_name']].append({
            'start_time': data['start_time'],
            'end_time': data['end_time']
        })

    def compute_gap(self, data):
        start_time = parser.isoparse(data['start_time'])
        end_time = parser.isoparse(data['end_time'])
        delta = end_time - start_time
        rounded_off = round(delta.total_seconds())

        logging.debug('Computing time gap between: Start date={} End date={} Total gap={}'.format(
            data['start_time'], data['end_time'], rounded_off))
        return rounded_off

    def compute_mean(self, durations):
        gaps = [self.compute_gap(gap) for gap in durations]
        return round(statistics.mean(gaps))

    def compute_standard_deviation(self, timegaps):
        gaps = [self.compute_gap(gap) for gap in timegaps]
        return round(statistics.stdev(gaps))

    def get_all_durations(self):
        gaps = []
        for key in self.reports.keys():
            gaps.extend(self.reports[key])
        return gaps

    def get_overall_mean(self):
        return self.compute_mean(self.get_all_durations())

    def get_overall_standard_deviation(self):
        return self.compute_standard_deviation(self.get_all_durations())

    def get_outlier_servers(self):
        standard_deviation_times_three = self.get_overall_standard_deviation() * 3
        outlier_lower_limit = self.get_overall_mean() - standard_deviation_times_three
        outlier_upper_limit = self.get_overall_mean() + standard_deviation_times_three
        logging.debug('Standard deviation: {}'.format(
            self.get_overall_standard_deviation()))
        logging.debug('Standard deviation times three: {}'.format(
            standard_deviation_times_three))
        logging.debug('Outlier lower limit: {}'.format(outlier_lower_limit))
        logging.debug('Outlier upper limit: {}'.format(outlier_upper_limit))
        servers = []
        for server in self.reports.keys():
            for duration in self.reports[server]:
                gap = self.compute_gap(duration)
                logging.debug('The gaps computed: ' + str(gap))
                if gap < outlier_lower_limit or gap > outlier_upper_limit:
                    servers.append(server)

        return servers

    def process_statistics(self):
        num_durations = len(self.get_all_durations())
        if num_durations >= 10:
            return {
                'mean': self.get_overall_mean(),
                'stddev': self.get_overall_standard_deviation()
            }
        else:
            return {
                'mean': '',
                'stddev': ''
            }
