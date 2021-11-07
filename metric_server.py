import json
from flask import Flask, request, abort, render_template
from metric_core import MetricCore

app = Flask(__name__)
metric_core = MetricCore()


@app.route('/process_report', methods=['POST'])
def process_report():
    data = request.get_json()
    app.logger.info('Received: Server name={} Start time={} End time={}'.format(data['server_name'], data['start_time'], data['end_time']))
    metric_core.store(data)
    return ""

@app.route('/process_statistics', methods=['GET'])
def process_statistics():
    statistics = metric_core.process_statistics()
    error_message = 'Cannot send report, not enough data ...'
    if(statistics['mean'] == '' or statistics['stddev'] == ''):
        app.logger.error(error_message)
        abort(500, 'Not enough reports received')
    else:
        return statistics


@app.route('/process_outliers', methods=['GET'])
def process_outliers():
    return json.dumps(metric_core.process_outliers())


@app.route('/', methods=['GET'])
def get_dashboard():
    statistics = metric_core.process_statistics()
    mean = 'NOT YET AVAILABLE...'
    standard_deviation = 'NOT YET AVAILABLE...'
    if statistics['mean']:
        mean = statistics['mean']
    if statistics['stddev']:
        standard_deviation = statistics['stddev']


    return render_template('index.html', 
    mean=mean, 
    standard_deviation=standard_deviation,
    outliers=metric_core.process_outliers())
