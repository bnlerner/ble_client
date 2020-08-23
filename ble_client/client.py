from pybleno import *
import sys
import signal
from ble_client.utilities import *
from ble_client.services.videoservice import VideoService
import time
print('ble service starting')

bleno = Bleno()


videoService = VideoService()

def onStateChange(state):
    print('on -> stateChange: ' + state)
    if (state == 'poweredOn'):
        bleno.startAdvertising('video', [videoService.uuid])
    else:
        bleno.stopAdvertising()
bleno.on('stateChange', onStateChange)

def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))
    if not error:
        def on_set_service_error(error):
            print('setServices: %s'  % ('error ' + error if error else 'success'))

        bleno.setServices([
            videoService
        ], on_set_service_error)
bleno.on('advertisingStart', onAdvertisingStart)

def main():
    
    bleno.start()
    time.sleep(100)    

    bleno.stopAdvertising()
    bleno.disconnect()
