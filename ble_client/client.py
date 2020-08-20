import bluepy
from bluepy.btle import DefaultDelegate, Peripheral

class NotificationDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print("A notification was received: %s" %data)


def main():
    print("hello world!")
    
    p = Peripheral("ee:6c:c1:cf:fe:f9", "public") # "random"

    p.setDelegate( NotificationDelegate() )

    # Setup to turn notifications on, e.g.
    svc = p.getServiceByUUID("47491010-1011-537e-4f6c-d104768a1001")
    ch = svc.getCharacteristics("uuid_char")[0]
    #ch_notify = svc.getCharacteristics()[1]
    p.writeCharacteristic(ch.valHandle + 1, "\x01\x00", withResponse=True)

    while True:
        if p.waitForNotifications(1.0):
            # handleNotification() was called
            print("got notification")
            continue

        print("Waiting...")
        # Perhaps do something else here
