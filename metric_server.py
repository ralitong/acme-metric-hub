import logging
import statistics
from dateutil import parser

class MetricServer:

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
        
        self.storage = {}


    def store(self, data):
        if not data['server_name'] in self.storage:
            self.storage[data['server_name']] = []
        
        logging.debug('Storing data: Server name={} Start date={} End date={}'.format(data['server_name'],data['start_time'], data['end_time']))

        self.storage[data['server_name']].append({
            'start_time': data['start_time'],
            'end_time': data['end_time']
        })
    
    def compute_gap(self, data):
        start_time = parser.isoparse(data['start_time'])
        end_time = parser.isoparse(data['end_time'])
        delta = end_time - start_time
        rounded_off = round(delta.total_seconds())

        logging.debug('Computing time gap between: Start date={} End date={} Total gap={}'.format(data['start_time'], data['end_time'], rounded_off))
        return rounded_off

    def compute_mean(self, timegaps):
        gaps = [  self.compute_gap(gap) for gap in timegaps]
        return round(statistics.mean(gaps))

    def compute_standard_deviation(self, timegaps):
        gaps = [  self.compute_gap(gap) for gap in timegaps]
        return round(statistics.stdev(gaps))











