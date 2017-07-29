from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from remote import SamsungRemote
import logging

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

    def _send_response(self, code, msg = None):
        print('Sending response {code}'.format(code = code))
        if code == 200:
            self.send_response(code)
        else:
            self.send_error(code, msg)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.flush()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(data_string.decode('utf-8'))
        logging.info(data['directive'])
        print('Received request {}'.format(data))
        try:
            namespace = data['directive']['header']['namespace']
            name = data['directive']['header']['name']
            payload = data['directive']['payload']
        except KeyError:
            logging.error('Bad request {}'.format(data))
            self._send_response(400)
            return
        remote = SamsungRemote()
        try:
            handler = self.command_handlers[(namespace, name)]
        except KeyError:
            errmsg = 'Unhandled command namespace = {namespace}, name = {name}'.format(name = name, namespace = namespace)
            logging.error(errmsg)
            self._send_response(400, errmsg)
            return
        self._send_response(200)
        handler(self, remote, payload)

def run(server_class=HTTPServer, handler_class=SamsungHttpHandler, port=81):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
