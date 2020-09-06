import json
import urllib.parse
import urllib.request
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from datetime import datetime
import nexmo
import messagebird

app = Flask(__name__)
api = Api(app)



def nexmoAPI(key,secret,messageTitle,recipient,message):
    client = nexmo.Client(key=key, secret=secret)

    client.send_message({
        'from': messageTitle,
        'to': recipient,
        'text': message
    })

def messageBirdAPI(key,messageTitle,recipient,message):
    client = messagebird.Client(key)
    message = client.message_create(
        messageTitle,
        recipient,
        message
    )
    print(message)

def telemessageAPI(username,password,recipient,message):
    url = "https://secure.telemessage.com/jsp/receiveSMS.jsp?userid=%s&password=%s&to=%s&text=%s" % (
    username, password, recipient, message)
    with urllib.request.urlopen(url) as f:
        if f.getcode() == 200:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S %z]")
            print("%s Sent SMS to %s" % (timestamp, recipient))


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

        try:
            if self.config['username'] !="" and self.config['provider'] !="":

                for a in content['alerts']:
                    prefix = "** "
                    if a['status'] in 'firing':
                        prefix = "** PROBLEM alert"

                    if a['status'] in 'resolved':
                        prefix = "** RECOVERY alert"

                    message = urllib.parse.quote("%s - %s\nURL: %s" % (prefix, a['labels'], a['generatorURL']))

                    for recipient in self.config['recipients']:
                        if self.config['provider'] == "nexmo":
                            nexmoAPI(self.config['username'], self.config['password'],self.config['messageTitle'], recipient, message)
                        elif self.config['provider'] == "telemessage":
                            messageBirdAPI(self.config['username'], self.config['messageTitle'], recipient, message)
                        elif self.config['provider'] == "messagebird":
                            telemessageAPI(self.config['username'],self.config['password'], self.config['messageTitle'], recipient, message)

            else:
                print("Missing User/Key or SMS Provider")
        except Exception as e:
            print(e)
api.add_resource(SMS, '/')
parser = reqparse.RequestParser()

if __name__ == '__main__':
    app.run(debug=True)
