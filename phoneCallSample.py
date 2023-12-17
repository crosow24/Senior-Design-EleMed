import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC38c976bd0b292236dbaa00a56bf2d1c1'
auth_token = '145eec63e9347e8de12760dbceb809de'
client = Client(account_sid, auth_token)

call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+12037278473',
                        from_='+18337780524'
                    )

print(call.sid)