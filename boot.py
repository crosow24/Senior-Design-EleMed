from BLE_CEEO import Yell, Listen
import time
import TwilioLibrary as lib

def peripheral(name):
    try:
        ssid = 'Unknown'
        password = 'Unknown'
        end = False
        wifiCheck = False
        p = Yell(name, verbose = True)
        if p.connect_up():
            print('P connected')
            time.sleep(2)
            while (wifiCheck == False):
                if p.is_any:
                    message = p.read()
                    if ssid == 'Unknown':
                        ssid = message
                        print('ssid')
                        print(ssid)
                    elif password == 'Unknown':
                        if (message == "None" or message == "NA" or message == "N/A" or message == "none"):
                            password = ''
                            print('password')
                            print(password)
                            end = True
                        else:
                            password = message
                            print('password')
                            print(password)
                            end = True
                if not p.is_connected:
                    print('lost connection')
                    break
                if end:
                    wifi = {'ssid':ssid,'pass':password}
                    print(wifi)
                    lib.connect_wifi(wifi)
                    try:
                        currentTime = lib.getTime()
                        print(currentTime)
                        user_data = lib.getUserData()
                        recipient_number = lib.parseData(user_data, 'Phone Number')
                        lib.send_sms(recipient_number,"Pad connected to wifi!")
                        payload = "Connected to wifi"
                        p.send(payload)
                        wifiCheck = True
                    except Exception as e:
                        print(e)
                time.sleep(1)
    except Exception as e:
        print(e)
    finally:
        p.disconnect()
        print('closing up')


peripheral('EleMedPad')
