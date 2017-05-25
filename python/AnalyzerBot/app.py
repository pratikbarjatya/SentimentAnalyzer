import os
import datetime
from flask import Flask, request
from twilio.rest import Client
import client

on_call = os.getenv('ON_CALL')
twilio_client = Client(os.getenv('TWILIO_ACCOUNT_KEY'), os.getenv('TWILIO_API_KEY'))


def send_message(body):
    twilio_client.messages.create(
        to=on_call,
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        body=body
    )

app = Flask(__name__)
sentiment_client = client.SentimentClient()

@app.route('/analyze', methods=['POST'])
def analyze():
    with open('logfile.txt', 'a') as fp_log:
        fp_log.write(request.form.get('text'))
        fp_log.write(sentiment_client.analyze(request.form.get('text')))
    return "Got it"


@app.route('/')
def health_check():
    return "Alive"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
