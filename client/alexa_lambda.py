#See https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/steps-to-create-a-smart-home-skill
import requests
import logging
SAMSUNG_SERVER_HOSTNAME = 'http://dwild428.hopto.org:81'

def lambda_handler(request, context):
    if request['directive']['header']['namespace'] == 'Alexa.Discovery' and request['directive']['header']['name'] == 'Discover':
        return handleDiscovery(request, context)
    else:
        return handleDirective(request, context)

def handleDiscovery(request, context):
    #Set Header
    header = request['directive']['header']
    header['name'] = "Discover.Response"

    #Set Payload
    endpoint = {
        "endpointId": "samsung_tv_id",
        "manufacturerName": "Samsung",
        "friendlyName": "TV",
        "description": "Left TV",
        "displayCategories": [  ],
        "cookie": {   },
        "capabilities":
            [
                {
                    "interface": "Alexa.PowerController",
                    "version": "1.0",
                    "type": "AlexaInterface"
                },
                {
                    "interface": "Alexa.ChannelController",
                    "version": "1.0",
                    "type": "AlexaInterface"
                },
                {
                    "interface": "Alexa.InputController",
                    "version": "1.0",
                    "type": "AlexaInterface"
                },
                {
                    "interface": "Alexa.PlaybackController",
                    "version": "1.0",
                    "type": "AlexaInterface"
                },
                {
                    "interface": "Alexa.StepSpeaker",
                    "version": "1.0",
                    "type": "AlexaInterface"
                }
            ]
    }
    payload = {'endpoints': [endpoint]}
    response = {'event': {'header': header, 'payload': payload}}
    return response

def handleDirective(request, context):
    httpResponse = requests.post(SAMSUNG_SERVER_HOSTNAME, json = request)
    if httpResponse:
        response = {
            "context": {
                "properties": []
            },
            "event": {
                "header": {
                    "messageId": request['directive']['header']['messageId'],
                    "namespace": "Alexa",
                    "name": "Response",
                    "payloadVersion": "3"
                },
                "payload": {}
            }
        }
        return response
    else:
        logging.error('Received response code {code}: {msg}'.format(code = httpResponse.status_code, msg = httpResponse.text))
        return None
