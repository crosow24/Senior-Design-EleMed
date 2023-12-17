import time
import math
import urequests as requests
import json

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
adc_change_threshold = 8000
moving_ave_value = measure()

currentTime = lib.getTime()
date = lib.getDate()
lib.postData(date,currentTime,'missed')

while True:
    print('listening')
    cur_val = measure()
    ave_counter = ave_counter + 1
    moving_ave_value = (moving_ave_value * (ave_counter-1) + cur_val) / ave_counter
    if abs(moving_ave_value - cur_val) > adc_change_threshold:
        print("triggered")
        currentTime = lib.getTime()
        date = lib.getDate()
        recordID = lib.mostRecentID()
        lib.patchDate(date, recordID)
        lib.patchTime(currentTime, recordID)
        lib.patchStatus('taken', recordID)
        time.sleep(10)
        moving_ave_value = measure()
        ave_counter = 1
        time.sleep(30)
        currentTime = lib.getTime()
        date = lib.getDate()
        lib.postData(date,currentTime,'missed')
    time.sleep(listening_freq)
