from pybleno import *
import sys
import signal
from utilities import *

print('bleno - echo')

bleno = Bleno()

def onStateChange(state):
    print('on -> stateChange: ' + state)
    if (state == 'poweredOn'):
        bleno.startAdvertising('echo', ['ec00'])
    else:
        bleno.stopAdvertising()

def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))
    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': 'ec00',
                'characteristics': [
                    BleCharacteristic('ec0F')
                    ]
            })
        ])

def main():
    
    bleno.on('stateChange', onStateChange)
    bleno.on('advertisingStart', onAdvertisingStart)
    bleno.start()


    bleno.stopAdvertising()
    bleno.disconnect()
