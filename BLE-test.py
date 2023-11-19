from BLE_CEEO import Yell, Listen
import time

def peripheral(name):
    try:
        p = Yell(name, verbose = True)
        if p.connect_up():
            print('P connected')
            time.sleep(2)
            payload = 'test'
            p.send(payload)
            while True:
                if p.is_any:
                    print(p.read())
                if not p.is_connected:
                    print('lost connection')
                    break
                time.sleep(1)
    except Exception as e:
        print(e)
    finally:
        p.disconnect()
        print('closing up')
def central(name):
    try:
        L = Listen(name, verbose = True)
        if L.connect_up():
            print('L connected')
            while L.is_connected:
                time.sleep(4)
                if L.is_any:
                    reply = L.read()
                    print(reply) #seems to stop at 80 characteres
                    L.send(reply[:20])  #seems to stop around 20 characters
    except Exception as e:
        print(e)
    finally:
        L.disconnect()
        print('closing up')

peripheral("Corey")


'''
Pseudocode
1. Connect to user cell phone as pheriperal
2. Wait in loop until wifi credentials are received
2.5. Test that credentials work and that the Pico can connect to the wifi
3. Once wifi credentials have been received, restart connection as a central
4. Connect with second pad to send wifi credentials
5. Kill BLE connection
'''
