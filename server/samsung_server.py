from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from remote import SamsungRemote
import logging

class SamsungHttpHandler(BaseHTTPRequestHandler):
    def handleAdjustVolume(self, samsungRemote, payload):
        samsungRemote.incrementVolume(int(payload['volumeSteps']))

    def handleMute(self, samsungRemote, payload):
        samsungRemote.toggleMute()

    def handlePower(self, samsungRemote, payload):
        samsungRemote.power()

    def handleSkipChannels(self, samsungRemote, payload):
        samsungRemote.incrementChannel(int(payload['channelCount']))

    command_handlers = {
        ('Alexa.PowerController', 'TurnOn'): handlePower,
        ('Alexa.PowerController', 'TurnOff'): handlePower,
        ('Alexa.StepSpeaker', 'AdjustVolume'): handleAdjustVolume,
        ('Alexa.StepSpeaker', 'SetMute'): handleMute,
        # ('Alexa.PlaybackController', 'FastForward'): handlePower,
        # ('Alexa.PlaybackController', 'Next'): handlePower,
        # ('Alexa.PlaybackController', 'Pause'): handlePower,
        # ('Alexa.PlaybackController', 'Play'): handlePower,
        # ('Alexa.PlaybackController', 'Previous'): handlePower,
        # ('Alexa.PlaybackController', 'Rewind'): handlePower,
        # ('Alexa.PlaybackController', 'StartOver'): handlePower,
        # ('Alexa.PlaybackController', 'Stop'): handlePower,
        ('Alexa.ChannelController', 'SkipChannels'): handleSkipChannels,
        #('Alexa.ChannelController', 'SkipChannels'): handleSkipChannels,
        ('Alexa.InputController', 'SelectInput'): handlePower

    }


    ##============================================================##

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # def do_GET(self):
    #     self._set_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(data_string.decode('utf-8'))
        try:
            namespace = data['directive']['header']['namespace']
            name = data['directive']['header']['name']
            payload = data['directive']['payload']
        except KeyError:
            logging.error('Bad request {}'.format(data))
            self.send_response(400)
            self.end_headers()
            return

        self.send_response(200)
        self.end_headers()

        remote = SamsungRemote()
        try:
            self.command_handlers[(namespace, name)](self, remote, payload)
        except KeyError:
            logging.error('Unhandled command namespace = {namespace}, name = {name}'.format(name = name, namespace = namespace))


def run(server_class=HTTPServer, handler_class=SamsungHttpHandler, port=80):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()