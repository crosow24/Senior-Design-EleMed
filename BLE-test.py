from BLE_CEEO import Yell, Listen
import time
import TwilioLibrary

def peripheral(name): 
    global ssid = "Unknown"
    global password = "Unknown"
    try:
        p = Yell(name, verbose = True)
        if p.connect_up():
            print('P connected')
            time.sleep(2)
            payload = 'test' 
            p.send(payload) 
            while (ssid == "Unknown" or password == "Unknown"):
                if p.is_any:
                    print(p.read())
                    if ssid == "Unknown":
                        ssid = p.read()
                    elif password == "Unknown":
                        if p.read() == "None" or p.read == "NA" 0r p.read == "N/A" or p.read == "none":
                            password = ""
                            end = True
                        else:
                            password = p.read()
                            end = True
                if not p.is_connected:
                    print('lost connection')
                    break
                if end:
                    global wifi = {'ssid':ssid,'pass':password}
                    TwilioLibrary.connect_wifi(wifi)
                    #test connect to AirTable API
                    #if fails, reset ssid and password to unknown and have user try again
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
                time.sleep(1)
                L.send(global wifi)  #seems to stop around 20 characters
    except Exception as e:
        print(e)
    finally:
        L.disconnect()
        print('closing up')
        

peripheral("EleMed Pad")
central("EleMed Pad")
    


'''
Pseudocode
1. Connect to user cell phone as pheriperal
2. Wait in loop until wifi credentials are received
2.5. Test that credentials work and that the Pico can connect to the wifi
3. Once wifi credentials have been received, restart connection as a central
4. Connect with second pad to send wifi credentials
5. Kill BLE connection
'''
