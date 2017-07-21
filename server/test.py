import unittest
import remote
import time

class Tester(unittest.TestCase):
    r = remote.SamsungRemote()
    r.goToChannel_slow(555)
    # r.toggleNumbers()
    # time.sleep(.8)
    # r.control('KEY_ENTER')  # 6
    # r.control('KEY_LEFT')
    # r.control('KEY_LEFT')
    # r.control('KEY_LEFT')
    # r.control('KEY_ENTER') #3
    # r.control('KEY_LEFT')
    # r.control('KEY_ENTER')
    # r.control('KEY_UP')
    # r.control('KEY_ENTER')

if __name__ == "__main__":
    unittest.main()
