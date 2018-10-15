from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import webbrowser
from dateutil import parser
from subprocess import check_output

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
  flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
  creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))
# Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 1 events')
events_result = service.events().list(calendarId='xxxxxx', timeMin=now,
                                    maxResults=2, singleEvents=True,
                                    orderBy='startTime').execute()
events = events_result.get('items', [])
if not events:
  print('No upcoming events found.')
for event in events:
  start = event['start'].get('dateTime', event['start'].get('date'))
  end = event['end'].get('dateTime', event['end'].get('date'))
  print('Event Found : ', event['summary'])
  if parser.parse(start,ignoretz=True) + datetime.timedelta(hours=3) <= datetime.datetime.now() + datetime.timedelta(minutes=2):
      if parser.parse(start,ignoretz=True) + datetime.timedelta(hours=3) > datetime.datetime.now() + datetime.timedelta(minutes=1):
          eventInfo = open('eventInfo.js','w')
          eventInfo.write("var endDate = new Date(new Date(\"" + end + "\") - 300000)")
          eventInfo.close()
          print('open the browser')
          webbrowser.open(event['hangoutLink'])
