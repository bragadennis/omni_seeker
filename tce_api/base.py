import requests
from models.tce_request_monitor import TceRequestMonitor
import json
from barely_json import parse
class Base:
    def __init__(self):
        self.base_url = 'https://api.tce.ce.gov.br/index.php/sim/1_0/'
        self.month = None

    def initialize_variables_by_method(self, method):
        self.method = method
        self.request_monitor = TceRequestMonitor.find_by_method(self.method)
        if self.request_monitor is None:
            self.year = 2015
            self.municipio_id = 0
        else:
            self.year = self.request_monitor.year
            self.municipio_id = self.request_monitor.municipio_id

    def request_tce_api(self, params = ''):
        return self.sanitize_response(
                        requests.get(
                            self.base_url + self.method + '.json' + params
                        ).text
                    )

    def save_progress(self, error, success):
        TceRequestMonitor.save_progress(
            self.request_monitor, self.method, self.year,
            self.month, self.error_message(error), success,
            self.municipio_id
        )

    def requestable(self):
        if self.request_monitor and self.request_monitor.success:
            return False
        return True

    def error_message(self, error):
        if error != '':
            error = str(type(error)).split("'")[1] + ':' +  str(error.args[0])
        return error

    def sanitize_response(self, text):
        try:
            return json.loads(text)
        except Exception as e:
            return parse(text)