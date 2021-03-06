import datetime
import logging
import random
import requests
import sys


class AcmeCore():

    def __init__(self, metric_server='http://localhost:8080', log_level='INFO'):
        self.set_log_level(log_level)
        self.name = self.generate_server_name()
        logging.debug('Server name: ' + self.name)
        self.normal_interval_lower = 1620
        self.normal_interval_upper = 1800
        self.unusual_interval_lower = 1400
        self.unusual_interval_upper = 2100
        self.metric_server = metric_server

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


    def generate_utc_date(self):
        now = datetime.datetime.utcnow()
        logging.debug('Generated UTC date: ' + now.isoformat())
        return now

    def generate_server_name(self):
        number = ''.join([str(random.randrange(9)) for x in range(9)])
        name = 't-' + number
        logging.debug('Generated Server name: ' + name)
        return name

    def generate_normal_interval(self):
        interval = random.randint(
            self.normal_interval_lower, self.normal_interval_upper)
        logging.debug('Random generated normal interval ' + str(interval))
        return interval

    def generate_unusual_interval(self):
        interval = random.randint(
            self.unusual_interval_lower, self.unusual_interval_upper)
        logging.debug('Random generated unusual interval ' + str(interval))
        return interval

    def generate_normal_time_interval(self):
        interval = self.generate_normal_interval()
        start = self.generate_utc_date()
        end = start + datetime.timedelta(seconds=interval)
        
        time_interval = {
            "start_time": start.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "end_time": end.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        logging.debug('Generated normal time interval: Start date={} End date={}'.format(time_interval['start_time'], time_interval['end_time']))
        return time_interval

    def generate_unusual_time_interval(self):
        interval = self.generate_unusual_interval()
        start = self.generate_utc_date()
        end = start + datetime.timedelta(seconds=interval)
        time_interval = {
            "start_time": start.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "end_time": end.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        logging.debug('Generated unusual time interval: Start date={} End date={}'.format(time_interval['start_time'], time_interval['end_time']))
        return time_interval

    def generate_normal_report(self):
        process = {
            "server_name" : self.name,
            **self.generate_normal_time_interval()
        }
        logging.debug('Generated normal batch process: Server name={} Start date={} End date={}'.format(process['server_name'],process['start_time'], process['end_time']))
        return process

    def generate_unusual_report(self):
        process = {
            "server_name" : self.name,
            **self.generate_unusual_time_interval()
        }
        logging.debug('Generated unusual batch process: Server name={} Start date={} End date={}'.format(process['server_name'],process['start_time'], process['end_time']))
        return process

    def post_normal_report(self):
        process = self.generate_normal_report()
        logging.info('Posting normal batch process: Server name={} Start date={} End date={} url={}'.format(process['server_name'],process['start_time'], process['end_time'], self.metric_server))

        try:
            requests.post(self.metric_server + '/process_report', json=process)
        except:
            logging.info('Posting normal batch process to {} failed, reason: {}'.format(self.metric_server, sys.exc_info()[0]))

    def post_unusual_report(self):
        process = self.generate_unusual_report()
        logging.info('Posting unusual batch process: Server name={} Start date={} End date={} url={}'.format(process['server_name'],process['start_time'], process['end_time'], self.metric_server))
        
        try:
            requests.post(self.metric_server + '/process_report', json=process)
        except:
            logging.info('Posting unusual batch process to {} failed, reason: {}'.format(self.metric_server, sys.exc_info()[0]))
