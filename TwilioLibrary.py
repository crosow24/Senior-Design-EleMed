import time
import network
import struct
import ubinascii
import urequests as requests
import umail
import mqtt
import json

from keys import account_sid
from keys import auth_token
from keys import email_password
from keys import base_id
from keys import AIRTABLE_URL
from keys import AIRTABLE_TOKEN
from keys import history_url
from keys import User_Info_url
from keys import sorted_history_url
from keys import headers as at_headers
from keys import Tufts_Wireless as wifi


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
def getUserData():
    response = requests.get(User_Info_url, headers = at_headers)
    print(response.status_code)
    data = response.json()
    return data
def postData(col_input1,col_input2,col_input3):
    #col_name = "Adherence_Status"
    #col_input = "missed" #eventually will
    data = {
        "records": [
            {
                "fields": {
                    'Date' : col_input1, 'Time' : col_input2, 'Adherence_Status' : col_input3,
                }
            }
        ]
    }
    response = requests.request("POST", history_url, headers=at_headers, data=json.dumps(data))
    print(response)
def patchData(field, col_input1, recordID):
    data = {
        "records": [
            {
                "id": recordID,
                "fields": {
                    field : col_input1,
                }
            }
        ]
    }
    response = requests.request("PATCH", history_url, headers=at_headers, data=json.dumps(data))
    code = response.json()
    print(code)
def patchDate(col_input1, recordID):
    data = {
        "records": [
            {
                "id": recordID,
                "fields": {
                    "Date" : col_input1,
                }
            }
        ]
    }
    response = requests.request("PATCH", history_url, headers=at_headers, data=json.dumps(data))
    code = response.json()
    print(code)
def patchTime(col_input1, recordID):
    data = {
        "records": [
            {
                "id": recordID,
                "fields": {
                    "Time" : col_input1,
                }
            }
        ]
    }
    response = requests.request("PATCH", history_url, headers=at_headers, data=json.dumps(data))
    code = response.json()
    print(code)
def patchStatus(col_input1, recordID):
    data = {
        "records": [
            {
                "id": recordID,
                "fields": {
                    "Adherence_Status" : col_input1,
                }
            }
        ]
    }
    response = requests.request("PATCH", history_url, headers=at_headers, data=json.dumps(data))
    code = response.json()
    print(code)
def AdheranceStatus():
    response = requests.get(sorted_history_url, headers = at_headers)
    data = response.json()
    length = len(data['records'])
    data=data['records'][length-1]['fields']['Adherence_Status']
    return data
def TimeTaken():
    response = requests.get(sorted_history_url, headers = at_headers)
    data = response.json()
    length = len(data['records'])
    data=data['records'][length-1]['fields']['Time']
    return data
def DateTaken():
    response = requests.get(sorted_history_url, headers = at_headers)
    data = response.json()
    length = len(data['records'])
    data=data['records'][length-1]['fields']['Date']
def mostRecentID():
    response = requests.get(sorted_history_url, headers = at_headers)
    data = response.json()
    length = len(data['records'])
    data=data['records'][length-1]['id']
    return data
def parseData(data, column):
    #pull data apart
    data=data['records'][0]['fields'][column]
    return data

time_headers = {
    'accept': 'application/json',
}
def getTime():
    response = requests.get('https://timeapi.io/api/Time/current/coordinate?latitude=38.9&longitude=-77.03', headers=time_headers)
    data=response.json()
    return (data['time'])
def getDate():
    response = requests.get('https://timeapi.io/api/Time/current/coordinate?latitude=38.9&longitude=-77.03', headers=time_headers)
    data=response.json()
    return (data['date'])
