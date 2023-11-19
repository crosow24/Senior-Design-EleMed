import time
import network
import struct
import ubinascii
import urequests as requests
import umail
import mqtt
from keys import account_sid
from keys import auth_token
from keys import email_password

def whenCalled(topic, msg):
    global wcdata
    print((topic.decode(), msg.decode()))
    # wcdata = (topic.decode(), msg.decode())
    wcdata = msg.decode()
    led.on()
    time.sleep(0.5)
    led.off()
def connect_wifi(wifi):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print("MAC " + mac)

    station.connect(wifi['ssid'],wifi['pass'])
    while not station.isconnected():
        time.sleep(1)
    print('Connection successful')
    print(station.ifconfig())
def send_sms(recipient,message):
    sender = '+1 833 7780 524'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = "To=" + recipient + "&From=" + sender + "&Body=" + message

    print("Attempting to send SMS")
    response = requests.post("https://api.twilio.com/2010-04-01/Accounts/" +
	                       account_sid + "/Messages.json",
	                       data=data,
	                       auth=(account_sid,auth_token),
	                       headers=headers)

    if response.status_code >= 300 or response.status_code < 200:
        print("There was an error with your request to send a message. \n" +
                      "Response Status: " + str(response.status_code))
    else:
        print("Success")
        print(response.status_code)
    response.close()
def send_email(recipient_email, message, sender_app_password):
    sender_email = 'elemedtufts@gmail.com'
    sender_name = 'EleMed Tufts'
    email_subject ='EleMed Medication Adherance Update'

    # Send email once after MCU boots up
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
    smtp.write("Subject:" + email_subject + "\n")
    smtp.write(message)
    smtp.send()
    smtp.quit()
def phone_call(recipient):
    print("not implemented yet")
    #fred = mqtt.MQTTClient('PicoTemp', 'io.adafruit.com', keepalive=60)
    #fred.connect()
    #fred.set_callback(whenCalled)
    #fred.publish('crosow24/feeds/temp',msg)
