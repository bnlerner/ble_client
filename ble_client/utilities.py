"""
This module offers some utilities, in a way they are work in both Python 2 and 3
"""

from pybleno import Characteristic
import array
import sys
import traceback
import binascii
import logging
from struct import unpack
import queue as queue

log = logging.getLogger(__name__)

queue = queue  # just to use it

class BleCharacteristic(Characteristic):

    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'write', 'notify'],
            'value': None
          })

        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None

    def onReadRequest(self, offset, callback):
        print('EchoCharacteristic - %s - onReadRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        callback(Characteristic.RESULT_SUCCESS, self._value[offset:])

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data
        print('EchoCharacteristic - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        if self._updateValueCallback:
            print('EchoCharacteristic - onWriteRequest: notifying')
            self._updateValueCallback(self._value)

        callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print('EchoCharacteristic - onSubscribe')
        self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        print('EchoCharacteristic - onUnsubscribe')
        self._updateValueCallback = None

def check_unpack(seq, index, pattern, size):
    """Check that we got size bytes, if so, unpack using pattern"""
    data = seq[index: index + size]
    assert len(data) == size, "Unexpected data len %d, expected %d" % (len(data), size)
    return unpack(pattern, data)[0]


def usbyte(seq, index):
    return check_unpack(seq, index, "<B", 1)


def ushort(seq, index):
    return check_unpack(seq, index, "<H", 2)


def usint(seq, index):
    return check_unpack(seq, index, "<I", 4)


def str2hex(data):  # we need it for python 2+3 compatibility
    # if sys.version_info[0] == 3:
    # data = bytes(data, 'ascii')
    if not isinstance(data, (bytes, bytearray)):
        data = bytes(data, "ascii")
    hexed = binascii.hexlify(data)
    return hexed
