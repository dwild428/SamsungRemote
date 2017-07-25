from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from remote import SamsungRemote
import logging
from threading import Thread

class SamsungHttpHandler(BaseHTTPRequestHandler):
    def handleAdjustVolume(self, samsungRemote, payload):
        steps = int(payload['volumeSteps'])
        #Default increment is 10, which is way too much
        if steps == 10:
            steps = 2
        elif steps == -10:
            steps = -2
        samsungRemote.incrementVolume(steps)

    def handleMute(self, samsungRemote, payload):
        samsungRemote.toggleMute()

    def handlePower(self, samsungRemote, payload):
        samsungRemote.power()

    def handleFastFoward(self, samsungRemote, payload):
        samsungRemote.fastforward()

    def handleRewind(self, samsungRemote, payload):
        samsungRemote.rewind()

    def handlePlay(self, samsungRemote, payload):
        samsungRemote.play()

    def handlePause(self, samsungRemote, payload):
        samsungRemote.pause()

    def handleSkipChannels(self, samsungRemote, payload):
        samsungRemote.incrementChannel(int(payload['channelCount']))

    def handleChangeChannels(self, samsungRemote, payload):
        channel = payload['channel']
        try:
            channelNumber = channel['number']
            samsungRemote.goToChannel(channelNumber)
            return
        except KeyError:
            pass
        channelName = ''
        channelName = channel.get('callSign')
        if not channelName:
            channelName = channel.get('affiliateCallSign')
        if not channelName:
            try:
                channelName = payload['channelMetadata']['name']
            except KeyError:
                pass
        if channelName:
            samsungRemote.goToChannelName(channelName)
        else:
            logging.error('Unable to extract channel from payload {}'.format(payload))


    command_handlers = {
        ('Alexa.PowerController', 'TurnOn'): handlePower,
        ('Alexa.PowerController', 'TurnOff'): handlePower,
        ('Alexa.StepSpeaker', 'AdjustVolume'): handleAdjustVolume,
        ('Alexa.StepSpeaker', 'SetMute'): handleMute,
        ('Alexa.PlaybackController', 'FastForward'): handleFastFoward,
        # ('Alexa.PlaybackController', 'Next'): handlePower,
        ('Alexa.PlaybackController', 'Pause'): handlePause,
        ('Alexa.PlaybackController', 'Play'): handlePlay,
        # ('Alexa.PlaybackController', 'Previous'): handlePower,
        ('Alexa.PlaybackController', 'Rewind'): handleRewind,
        # ('Alexa.PlaybackController', 'StartOver'): handlePower,
        # ('Alexa.PlaybackController', 'Stop'): handlePower,
        ('Alexa.ChannelController', 'SkipChannels'): handleSkipChannels,
        ('Alexa.ChannelController', 'ChangeChannel'): handleChangeChannels,
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
        logging.info(data['directive'])
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
            handler = Thread(target=self.command_handlers[(namespace, name)](self, remote, payload))
        except KeyError:
            logging.error('Unhandled command namespace = {namespace}, name = {name}'.format(name = name, namespace = namespace))
        handler.start()

def run(server_class=HTTPServer, handler_class=SamsungHttpHandler, port=81):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()