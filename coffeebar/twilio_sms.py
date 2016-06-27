import os

import twilio.rest


class TwilioMessage(object):
    def __init__(self):
        self.__client = twilio.rest.TwilioRestClient(
            os.environ['TWILIO_ACCOUNT_SID'],
            os.environ['TWILIO_AUTH_TOKEN'])
        self.__to = os.environ['TO_PHONE_NUMBER']
        self.__from = os.environ['FROM_PHONE_NUMBER']

    def send(self, body):
        self.__client.messages.create(to=self.__to, from_=self.__from, body=body)
