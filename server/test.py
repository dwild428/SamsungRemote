import unittest
import remote
import time

class Tester(unittest.TestCase):
    r = remote.SamsungRemote()
    #r.goToChannel(555)
    r.goToChannel(20)

if __name__ == "__main__":
    unittest.main()
