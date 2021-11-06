from flask import Flask
from flask import request
from metric_core import MetricCore
import logging
import json

app = Flask(__name__)
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
metric_core = MetricCore()


@app.route('/process_report', methods=['POST'])
def process_report():
    data = request.get_json()
    app.logger.info('Received: Server name={} Start time={} End time={}'.format(data['server_name'], data['start_time'], data['end_time']))
    metric_core.store(data)
    return ""