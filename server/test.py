import unittest
import time
import requests

class Tester(unittest.TestCase):
    SAMSUNG_SERVER_HOSTNAME = 'http://dwild428.hopto.org:81'
    request = {
        "directive": {
            "header": {
                "namespace": "Alexa.StepSpeaker",
                "name": "AdjustVolume",
                "messageId": "c8d53423-b49b-48ee-9181-f50acedf2870",
                "payloadVersion": "3"
            },
            "endpoint": {
                "scope": {
                    "type": "BearerToken",
                    "token": "some-access-token"
                },
                "endpointId": "device-001",
                "cookie": {

                }
            },
            "payload": {
                "volumeSteps": -10
            }
        }
    }
    requests.post('http://dwild428.hopto.org:81', json=request, timeout = 10)

if __name__ == "__main__":
    unittest.main()
