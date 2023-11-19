from BLE_CEEO import Yell, Listen
import time
import TwilioLibrary

def peripheral(name):
    try:
        connected = False
        p = Yell(name, verbose = True)
        if p.connect_up():
            print('P connected')
            time.sleep(2)
            payload = 'test'
            p.send(payload)
            while !connected:
                if p.is_any:
                    time.sleep(1)
                    print(p.read())
                    global wifi = p.read()
                    TwilioLibrary.connect_wifi(wifi)
                    #test connect to AirTable API
                    #if fails, reset and wait for next transmission
                if not p.is_connected:
                    print('lost connection')
                    break
                time.sleep(1)

peripheral("EleMed Pad")
