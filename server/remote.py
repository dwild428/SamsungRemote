import samsungctl
import time
import subprocess
import logging

STATIC_IP = '192.168.0.15'
PUBLIC_HOSTNAME = 'dwild428.hopto.org'

def getIp(mac_address):
    arp = subprocess.Popen(('arp', '-a'), stdout=subprocess.PIPE)
    try:
        output = subprocess.check_output(('FINDSTR', mac_address), stdin=arp.stdout)
    except subprocess.CalledProcessError:
        print('Unable to find device')
        return
    if not output:
        print('Unable to find device')
        return
    return output.split()[0].decode('utf-8')


class SamsungRemote:
    def __init__(self, ip=STATIC_IP, port=8001):
        self.config = {
            "name": "samsungctl",
            "description": "Alexa",
            "id": "",
            "host": ip,
            "port": port,
            "method": "websocket",
            "timeout": 3,
        }

    def _remote(self, delay = 0.5):
        samsungctl.remote_websocket.RemoteWebsocket._key_interval = delay
        r = samsungctl.Remote(self.config)
        return r

    def incrementVolume(self, n=1):
        with self._remote(delay = .3) as remote:
            if n > 0:
                for i in range(n):
                    remote.control('KEY_VOLUP')
            else:
                for i in range(n*-1):
                    remote.control('KEY_VOLDOWN')

    def toggleMute(self):
        with self._remote(delay = 1) as remote:
            remote.control('KEY_MUTE')

    def incrementChannel(self, n=1):
        with self._remote(delay = .3) as remote:
            if n > 0:
                for i in range(n):
                    remote.control('KEY_CHUP')
            else:
                for i in range(n * -1):
                    remote.control('KEY_CHDOWN')

    def lastChannel(self):
        with self._remote() as remote:
            remote.control('KEY_RETURN')

    def goToChannel_fast(self, n):
        with self._remote() as remote:
            for digit in str(n):
                time.sleep(.9)
                remote.control('KEY_%s' % digit)
            remote.control("KEY_ENTER")

    def goToChannel(self, n):
        with self._remote(delay = 0.3) as remote:
            remote.control('KEY_MORE')
            time.sleep(1.5)
            prev = 6
            for i in str(n):
                num = int(i)
                if num == 0:
                    num = 10
                for j in range(abs(prev - num)):
                    if num > prev:
                        remote.control('KEY_RIGHT')
                    else:
                        remote.control('KEY_LEFT')
                prev = num
                remote.control('KEY_ENTER')
            remote.control('KEY_UP')
            remote.control('KEY_ENTER')

    def goToChannelName(self, channelName):
        try:
            channel = CHANNEL_LIST[channelName.upper()]
            self.goToChannel(channel)
        except KeyError:
            logging.error('Unable to find channel with name {}'.format(channelName))

    def power(self):
        with self._remote() as remote:
            remote.control("KEY_POWER")

    def toggleNumbers(self):
        with self._remote() as remote:
            remote.control('KEY_MORE')

    def pause(self):
        with self._remote(delay = 1) as remote:
            remote.control('KEY_PAUSE')

    def play(self):
        with self._remote(delay = 1) as remote:
            remote.control('KEY_PLAY')

    def record(self):
        with self._remote() as remote:
            remote.control('KEY_REC')

    def fastfoward(self, speed = 2):
        with self._remote() as remote:
            for i in range(speed):
                remote.control('KEY_FF')

    def rewind(self, speed = 2):
        with self._remote() as remote:
            for i in range(speed):
                remote.control('KEY_REWIND')

CHANNEL_LIST = {
    'HSN': 601,
    'WCBS': 602,
    'WNBC': 604,
    'FOX NEW YORK': 605,
    'FOX': 605,
    'UNIVISION': 606,
    'WABC': 607,
    'ABC': 607,
    'MY NINE': 609,
    'THE CW NEW YORK': 611,
    'CW NEW YORK': 611,
    'QVC': 612,
    'PBS': 613,
    'WFUT': 614,
    'ION': 615,
    'WRNN': 616,
    'TELEMUNDO': 617,
    'LIVEWELL': 618,
    'BET': 619,
    'A AND E': 620,
    'BRAVO': 621,
    'TBS': 622,
    'TNT': 623,
    'USA': 624,
    'SPIKE TV': 625,
    'FX': 626,
    'WGN AMERICA': 627,
    'MAVTV': 628,
    'SYFY': 630,
    'ANIMAL PLANET': 631,
    'COMEDY CENTRAL': 632,
    'CARTOON NETWORK': 633,
    'FUSE': 635,
    'E': 637,
    'WE TV': 638,
    'LIFETIME': 639,
    'LIFETIME MOVIE NETWORK': 640,
    'FREEFORM': 641,
    'FOOD NETWORK': 642,
    'HGTV': 643,
    'HALLMARK CHANNEL': 644,
    'DESTINATION AMERICA': 645,
    'DISNEY JUNIOR': 646,
    'DISNEY CHANNEL': 647,
    'DISNEY XD': 648,
    'NICKELODEON': 649,
    'CNN': 650,
    'CNBC': 651,
    'MSNBC': 652,
    'FOX NEWS CHANNEL': 653,
    'FOX NEWS': 653,
    'FOX BUSINESS NETWORK': 654,
    'FOX BUSINESS': 654,
    'THE WEATHER CHANNEL': 655,
    'HLN': 656,
    'HALLMARK MOVIE AND MYSTERY': 657,
    'TRUTV': 658,
    'INVESTIGATIVE DISCOVERY': 659,
    'TRAVEL CHANNEL': 660,
    'DISCOVERY': 661,
    'HISTORY CHANNEL': 662,
    'TLC': 663,
    'FYI': 664,
    'CRIME AND INVESTIGATION': 665,
    'IFC': 666,
    'AMC': 667,
    'STARZ ENCORE': 668,
    'TV LAND': 669,
    'NATIONAL GEOGRAPHIC': 670,
    'SCIENCE': 671,
    'BLOOMBERG': 672,
    'GSN': 673,
    'MTV2': 674,
    'MTV TWO': 674,
    'MTV': 675,
    'VH1': 676,
    'CMT': 677,
    'MSG OVERFLOW': 678,
    'MSG PLUS OVERFLOW': 679,
    'ESPNU': 680,
    'ESPN': 681,
    'ESPN 2': 682,
    'ESPN TWO': 682,
    'ESPN NEWS': 683,
    'NFL RED ZONE': 684,
    'RED ZONE': 684,
    'SPORTSNET NEW YORK': 685,
    'YES': 686,
    'MSG': 687,
    'MSG PLUS': 688,
    'FOX SPORTS': 689,
    'NFL NETWORK': 690,
    'NBC SPORTS NETWORK': 691,
    'TENNIS CHANNEL': 692,
    'NHL NETWORK': 693,
    'GOLF CHANNEL': 694,
    'MLB NETWORK': 695,
    'OUTDOOR CHANNEL': 696,
    'NBA TV': 697,
    'FXX': 698
}
'''
KEY_0
KEY_1
KEY_2
KEY_3
KEY_4
KEY_5
KEY_6
KEY_7
KEY_8
KEY_9
KEY_11
KEY_12
KEY_3SPEED
KEY_4_3
KEY_16_9
KEY_AD
KEY_ADDDEL
KEY_ALT_MHP
KEY_ANGLE
KEY_ANTENA
KEY_ANYNET
KEY_ANYVIEW
KEY_APP_LIST
KEY_ASPECT
KEY_AUTO_ARC_ANTENNA_AIR
KEY_AUTO_ARC_ANTENNA_CABLE
KEY_AUTO_ARC_ANTENNA_SATELLITE
KEY_AUTO_ARC_ANYNET_AUTO_START
KEY_AUTO_ARC_ANYNET_MODE_OK
KEY_AUTO_ARC_AUTOCOLOR_FAIL
KEY_AUTO_ARC_AUTOCOLOR_SUCCESS
KEY_AUTO_ARC_CAPTION_ENG
KEY_AUTO_ARC_CAPTION_KOR
KEY_AUTO_ARC_CAPTION_OFF
KEY_AUTO_ARC_CAPTION_ON
KEY_AUTO_ARC_C_FORCE_AGING
KEY_AUTO_ARC_JACK_IDENT
KEY_AUTO_ARC_LNA_OFF
KEY_AUTO_ARC_LNA_ON
KEY_AUTO_ARC_PIP_CH_CHANGE
KEY_AUTO_ARC_PIP_DOUBLE
KEY_AUTO_ARC_PIP_LARGE
KEY_AUTO_ARC_PIP_LEFT_BOTTOM
KEY_AUTO_ARC_PIP_LEFT_TOP
KEY_AUTO_ARC_PIP_RIGHT_BOTTOM
KEY_AUTO_ARC_PIP_RIGHT_TOP
KEY_AUTO_ARC_PIP_SMALL
KEY_AUTO_ARC_PIP_SOURCE_CHANGE
KEY_AUTO_ARC_PIP_WIDE
KEY_AUTO_ARC_RESET
KEY_AUTO_ARC_USBJACK_INSPECT
KEY_AUTO_FORMAT
KEY_AUTO_PROGRAM
KEY_AV1
KEY_AV2
KEY_AV3
KEY_BACK_MHP
KEY_BOOKMARK
KEY_CALLER_ID
KEY_CAPTION
KEY_CATV_MODE
KEY_CHDOWN
KEY_CHUP
KEY_CH_LIST
KEY_CLEAR
KEY_CLOCK_DISPLAY
KEY_COMPONENT1
KEY_COMPONENT2
KEY_CONTENTS
KEY_CONVERGENCE
KEY_CONVERT_AUDIO_MAINSUB
KEY_CUSTOM
KEY_CYAN
KEY_DEVICE_CONNECT
KEY_DISC_MENU
KEY_DMA
KEY_DNET
KEY_DNIe
KEY_DNSe
KEY_DOOR
KEY_DOWN
KEY_DSS_MODE
KEY_DTV
KEY_DTV_LINK
KEY_DTV_SIGNAL
KEY_DVD_MODE
KEY_DVI
KEY_DVR
KEY_DVR_MENU
KEY_DYNAMIC
KEY_ENTER
KEY_ENTERTAINMENT
KEY_ESAVING
KEY_EXIT
KEY_EXT1
KEY_EXT2
KEY_EXT3
KEY_EXT4
KEY_EXT5
KEY_EXT6
KEY_EXT7
KEY_EXT8
KEY_EXT9
KEY_EXT10
KEY_EXT11
KEY_EXT12
KEY_EXT13
KEY_EXT14
KEY_EXT15
KEY_EXT16
KEY_EXT17
KEY_EXT18
KEY_EXT19
KEY_EXT20
KEY_EXT21
KEY_EXT22
KEY_EXT23
KEY_EXT24
KEY_EXT25
KEY_EXT26
KEY_EXT27
KEY_EXT28
KEY_EXT29
KEY_EXT30
KEY_EXT31
KEY_EXT32
KEY_EXT33
KEY_EXT34
KEY_EXT35
KEY_EXT36
KEY_EXT37
KEY_EXT38
KEY_EXT39
KEY_EXT40
KEY_EXT41
KEY_FACTORY
KEY_FAVCH
KEY_FF
KEY_FF_
KEY_FM_RADIO
KEY_GAME
KEY_GREEN
KEY_GUIDE
KEY_HDMI
KEY_HDMI1
KEY_HDMI2
KEY_HDMI3
KEY_HDMI4
KEY_HELP
KEY_HOME
KEY_ID_INPUT
KEY_ID_SETUP
KEY_INFO
KEY_INSTANT_REPLAY
KEY_LEFT
KEY_LINK
KEY_LIVE
KEY_MAGIC_BRIGHT
KEY_MAGIC_CHANNEL
KEY_MDC
KEY_MENU
KEY_MIC
KEY_MORE
KEY_MOVIE1
KEY_MS
KEY_MTS
KEY_MUTE
KEY_NINE_SEPERATE
KEY_OPEN
KEY_PANNEL_CHDOWN
KEY_PANNEL_CHUP
KEY_PANNEL_ENTER
KEY_PANNEL_MENU
KEY_PANNEL_POWER
KEY_PANNEL_SOURCE
KEY_PANNEL_VOLDOW
KEY_PANNEL_VOLUP
KEY_PANORAMA
KEY_PAUSE
KEY_PCMODE
KEY_PERPECT_FOCUS
KEY_PICTURE_SIZE
KEY_PIP_CHDOWN
KEY_PIP_CHUP
KEY_PIP_ONOFF
KEY_PIP_SCAN
KEY_PIP_SIZE
KEY_PIP_SWAP
KEY_PLAY
KEY_PLUS100
KEY_PMODE
KEY_POWER
KEY_POWEROFF
KEY_POWERON
KEY_PRECH
KEY_PRINT
KEY_PROGRAM
KEY_QUICK_REPLAY
KEY_REC
KEY_RED
KEY_REPEAT
KEY_RESERVED1
KEY_RETURN
KEY_REWIND
KEY_REWIND_
KEY_RIGHT
KEY_RSS
KEY_RSURF
KEY_SCALE
KEY_SEFFECT
KEY_SETUP_CLOCK_TIMER
KEY_SLEEP
KEY_SOUND_MODE
KEY_SOURCE
KEY_SRS
KEY_STANDARD
KEY_STB_MODE
KEY_STILL_PICTURE
KEY_STOP
KEY_SUB_TITLE
KEY_SVIDEO1
KEY_SVIDEO2
KEY_SVIDEO3
KEY_TOOLS
KEY_TOPMENU
KEY_TTX_MIX
KEY_TTX_SUBFACE
KEY_TURBO
KEY_TV
KEY_TV_MODE
KEY_UP
KEY_VCHIP
KEY_VCR_MODE
KEY_VOLDOWN
KEY_VOLUP
KEY_WHEEL_LEFT
KEY_WHEEL_RIGHT
KEY_W_LINK
KEY_YELLOW
KEY_ZOOM1
KEY_ZOOM2
KEY_ZOOM_IN
KEY_ZOOM_MOVE
KEY_ZOOM_OUT
'''