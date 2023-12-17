import time
import math

from machine import Pin, PWM
from keys import Tufts_Wireless as wifi
import TwilioLibrary as lib
from keys import email_password

time.sleep(10)

lib.connect_wifi(wifi)

s12 = machine.ADC(28)
s34 = machine.ADC(26)

def measure():
    weight = s12.read_u16() + s34.read_u16()
    return weight

listening_freq = .05
ave_counter = 1
adc_change_threshold = 20000
moving_ave_value = measure()

while True:
    print('listening')
    cur_val = measure()
    ave_counter = ave_counter + 1
    moving_ave_value = (moving_ave_value * (ave_counter-1) + cur_val) / ave_counter
    if abs(moving_ave_value - cur_val) > adc_change_threshold:
        print("triggered")
        #check notifcation type and get user data
        user_data = lib.getUserData()
        status = lib.AdheranceStatus()
        print(status)
        if status == 'missed':
            notify_method = lib.parseData(user_data, 'Reminder Type')
            print(notify_method)
            print('get here')
            currentTime = lib.getTime()
            date = lib.getDate()
            recordID = lib.mostRecentID()
            lib.patchDate(date, recordID)
            lib.patchTime(currentTime, recordID)
            if notify_method == "Email":
                recipient_email = lib.parseData(user_data, 'Email')
                lib.send_email(recipient_email,"Meds Missed! Take them now!", email_password)
            if notify_method == "Text":
                recipient_number = lib.parseData(user_data, 'Phone Number')
                lib.send_sms(recipient_number,"Meds Missed! Take them now!")
            time.sleep(30)
        time.sleep(10)
        moving_ave_value = measure()
        ave_counter = 1
    time.sleep(listening_freq)
