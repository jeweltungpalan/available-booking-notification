import requests
import json
import time
import datetime
from twilio.rest import Client
import http.client
import mimetypes
import json

account_sid = '' #enter twilio account number here
auth_token = '' #enter twilio auth token here
client = Client(account_sid, auth_token)

end = datetime.datetime(2021, 4, 30)
now = datetime.datetime.now()
available = False

while now < end:
    end = end.strftime('%Y-%m-%d')
    today = datetime.date.today().strftime('%Y-%m-%d')
    print(now)

    conn = http.client.HTTPSConnection("www.passport.gov.ph")
    payload = ''
    headers = {
    'Cookie': 'BIGipServerpool_OAS=369889452.20480.0000; TS015a4cf5=01c23a1d8bb2dec1d433de850c192bf8da064a4cb4c00fbb517cf1e6d5eb021307a1f7ba5761d31b92a425ef313c631f024839ec72'
    }
    conn.request("POST", "/appointment/timeslot/available?fromDate=" + today + "&toDate=" + end + "&siteId=7&requestedSlots=1", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    json_obj = json.loads(data)

    now = datetime.datetime.now()

    for x in json_obj:
        availability=x['IsAvailable']
        appointmentDate=x['AppointmentDate']

        if availability == True:
            message = client.messages.create(
               body='New passport appointment opening found.',
               from_='+12566734367',
               to='' #enter phone number here
            )
            print('Available')
            available = True
            break
    
    if available == True:
        break

    if available == False:
        print("No openings. Rerunning in 360 seconds...")
        time.sleep(360)