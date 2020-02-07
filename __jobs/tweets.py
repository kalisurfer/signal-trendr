from datetime import datetime, timedelta
import smtplib
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback



SENDER_ADDRESS = "robot@decoursey.net"
HOST = "rrt5-kbxp.accessdomain.com"
USERNAME = "robot@decoursey.net"
PASSWORD = "1@m@R0b0t"
USE_SSL = True
PORT = 587


timestamp = datetime.utcnow()
now = timestamp - timedelta(minutes=timestamp.minute,
			seconds=timestamp.second,
			microseconds=timestamp.microsecond)

OK = True
message = "OK"

try:
	from ingest import Ingestion # , tweetCollection, gamesCollection, ObjectId, gameHistory
	consumer = Ingestion(now)
except Exception as e:
	type, value, tb = sys.exc_info()
	message = traceback.format_exc(tb)
	OK = False
	message += "\r\n{0}".format(str(e))
	tb = None
	type = None
	value = None

try:
	from events import EventProcessor
	prochester = EventProcessor()
	prochester.analyze_all_games()
except Exception as e:
	type, value, tb = sys.exc_info()
	if message == "OK":
		message = ""
	message += traceback.format_exc(tb)
	OK = False
	message += "\r\n{0}".format(str(e))
	tb = None
	type = None
	value = None

try:
	from movers import shakers
	message += "\r\n\r\n" + shakers(now)
except Exception as e:
	type, value, tb = sys.exc_info()
	if message == "OK":
		message = ""
	message += traceback.format_exc(tb)
	OK = False
	message += "\r\n{0}".format(str(e))
	tb = None
	type = None
	value = None



print message

def send_mail(subject, recipient, text, html):
	try:
		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From'] = SENDER_ADDRESS
		msg['To'] = recipient
		if text:
			msg.attach(MIMEText(text, 'plain'))
		if html:
			msg.attach(MIMEText(html, 'html'))
		smtp = smtplib.SMTP(HOST, port=PORT, timeout=20)
		if USERNAME and PASSWORD:
			try:
				smtp.login(USERNAME, PASSWORD)
			except Exception as e:
				pass
		smtp.sendmail(msg["From"], msg["To"], msg.as_string())
	except Exception as e:
		return str(e)


print send_mail("[tweets] I just ran", "sean.net@gmail.com", message, None)
print send_mail("[tweets] I just ran", "cancer@decoursey.net", message, None)


from discovery import what_are_they_talking_about, tag_and_discover

what_message = what_are_they_talking_about()
disc_message = tag_and_discover()
message = u"KEYWORD Matches\r\n\r\n\r\n{1}\r\n\r\n\r\nWhat are they talking about?\r\n\r\n{0}".format(what_message, disc_message).encode("utf8")
print send_mail("[keyword] matches in the last hour", "sean.net@gmail.com", message, None)
print send_mail("[keyword] matches in the last hour", "cancer@decoursey.net", message, None)



