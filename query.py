#!/usr/bin/python

from m2x.client import M2XClient
from datetime import datetime, timedelta
import pytz

def sendSMS(tonum, txt):

  from twilio.rest import TwilioRestClient

  account = ""
  token = ""
  client = TwilioRestClient(account, token)

  message = client.sms.messages.create(to="+1" + tonum, from_="+12147363810", body=txt)

apikey = ''
feedid = ''

client = M2XClient(key=apikey)

feed = client.feeds.details(feedid)

#devicemap = {'deadbeef0000': 'Mike\'s watch', 'feedbeef0000': 'Macbook Pro', '001122334455': 'Closet safe'}
devicemap = {'78C5E56E90BC': 'Macbook Pro', '0022D00002BD': "John"}


currenttime = datetime.now(pytz.utc)

print "<html>"
print "<head>"
print "<meta http-equiv=\"refresh\" content=\"10\">"
print "<title>SmartSentry Status</title></head>"
print "<body>"
  
print "<h1>SmartSentry Status</h1>"
print "<h3>Last updated: " + currenttime.strftime('%Y-%m-%d %H:%M:%S') + "</h3>"
print "<table border=1 cellpadding='10'>"
print "<tr><td width=33%>Name</td><td width=33%>Last seen</td><td width=33%>Status</td></tr>"


for stream in feed.streams:
  #for value in stream.values:
  #  print '{0} - {1}'.format(stream.name, value.at.strftime('%Y-%m-%d %H:%M:%S'))
  #print '{0} - {1}'.format(stream.name, stream.updated.strftime('%Y-%m-%d %H:%M:%S'))
  status = "Good"
  k = stream.name.encode('ascii', 'ignore').upper()
  if (k == '0022D00002BD'):
    status = "At Home" 
  if stream.updated < currenttime - timedelta(seconds=30):
    
    if (k == '0022D00002BD'):
      msg = "ALERT!\n" + devicemap[k] + " left the house around " + stream.updated.strftime('%Y-%m-%d %H:%M:%S') + ".  Turning down thermostat and waiting for his return."
      status = "Not in house"
      sendSMS("phone1", msg)
      print "<tr><td>" + devicemap[k] + "</td><td>" + stream.updated.strftime('%Y-%m-%d %H:%M:%S') + "</td><td>" + status + "<BR>Alert sent to Mike, thermostat has been turned down.</td></tr>"
    else:
      msg = "ALERT!\n" + devicemap[k] + " has not been seen since " + stream.updated.strftime('%Y-%m-%d %H:%M:%S') + ".  You may want to look for it!"
      status = "Missing!"
      sendSMS("phone2", msg) 
      print "<tr><td>" + devicemap[k] + "</td><td>" + stream.updated.strftime('%Y-%m-%d %H:%M:%S') + "</td><td>" + status + "<BR>Alert sent to Himanshu</td></tr>"
  else:
    print "<tr><td>" + devicemap[k] + "</td><td>" + stream.updated.strftime('%Y-%m-%d %H:%M:%S') + "</td><td>" + status + "</td></tr>"

print "</table>"
print "</body>"
print "</html>"

