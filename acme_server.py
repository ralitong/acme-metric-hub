import datetime
import logging
import random

class AcmeServer():

    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
        self.name = self.generate_server_name()
        logging.debug('Server name: ' + self.name)
        self.normal_interval_lower = 1620
        self.normal_interval_upper = 1800
        self.unusual_interval_lower = 1500
        self.unusual_interval_upper = 2100


    def generate_batch_request(self):
        pass

    def generate_utc_date(self):
        now = datetime.datetime.utcnow()
        logging.debug('Generated UTC date: ' + now.isoformat())
        return now

    def generate_server_name(self):
        number = ''.join([str(random.randrange(10)) for x in range(10)])
        name = 't-' + number
        logging.debug('Generated Server name: ' + name)
        return name

    def generate_normal_interval(self):
        interval = random.randint(self.normal_interval_lower, self.normal_interval_upper)
        logging.debug('Random generated normal interval ' + str(interval))
        return interval
    
    def generate_unusual_interval(self):
        interval = random.randint(self.unusual_interval_lower, self.unusual_interval_upper)
        logging.debug('Random generated unusual interval ' + str(interval))
        return interval
        
    


    


    


