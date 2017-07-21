import unittest
import remote

class Tester(unittest.TestCase):
    r = remote.SamsungRemote()
    r.goToChannel(632)

if __name__ == "__main__":
    unittest.main()
