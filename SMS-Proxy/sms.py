import json
import urllib.parse
import urllib.request
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from datetime import datetime

app = Flask(__name__)
api = Api(app)

class SMS(Resource):
    config = dict()

    def __init__(self):
        self.get_config()

    def get(self):
        return "SMS Proxy. Use POST (https://prometheus.io/docs/alerting/configuration/#webhook_config)."

    def get_config(self):
        with open('config') as f:
            self.config = json.load(f)

    def post(self):
        args = parser.parse_args()
        content = request.json
        for a in content['alerts']:
            prefix = "** "
            if a['status'] in 'firing':
                prefix = "** PROBLEM alert"

            if a['status'] in 'resolved':
                prefix = "** RECOVERY alert"
           
            message = urllib.parse.quote("%s - %s\nURL: %s" % (prefix, a['labels'], a['generatorURL']))

            for recipient in self.config['recipients']:
                url = "https://secure.telemessage.com/jsp/receiveSMS.jsp?userid=%s&password=%s&to=%s&text=%s" % (self.config['username'],self.config['password'],recipient,message)
                with urllib.request.urlopen(url) as f:
                    if f.getcode() == 200:
                        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S %z]")
                        print("%s Sent SMS to %s" % (timestamp, recipient))

api.add_resource(SMS, '/')
parser = reqparse.RequestParser()

if __name__ == '__main__':
    app.run(debug=True)
