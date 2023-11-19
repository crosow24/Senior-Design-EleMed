import TwilioLibrary
from keys import Tufts_Wireless as wifi
from keys import email_password
import time

userPhone="+1 203 727 8473"
userEmail="connor.rosow@gmail.com"
standardMessage="You have made breakfast without taking your morning medication, please take your medication now!"

TwilioLibrary.connect_wifi(wifi)
#TwilioLibrary.send_sms(userPhone, standardMessage)
#time.sleep(5)
TwilioLibrary.send_email(userEmail,standardMessage, email_password)

'''
Pseudocode:
1. Function for setup (ble stuff, sensor calibration, etc.)
2. Sleep function (basically set a sleep statement based on current time and set wake up time
3. Function for reading sensors
 - This will include calls to the notification functions in TwilioLibrary

Needs: separate library handling airtable/adherance history
'''
