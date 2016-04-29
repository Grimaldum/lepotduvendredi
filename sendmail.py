import config
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import urllib, json, random

giphyurl = GIPHYURLBEG
giphykws = ""

for kw in GIPHYKEYWORDS:
  giphykws += kw
  giphykws += "+"

giphykws[:-1]
giphyurl += giphykws
giphyurl += GIPHYURLEND

response = urllib.urlopen(giphyurl)
giphydata = json.loads(response.read())
giftotal = len(giphydata['data'])
gifurl = giphydata['data'][random.randint(0, giftotal-1)]['images']['fixed_height']['url']
img = urllib.urlopen(gifurl).read()

msgImg = MIMEImage(img, 'gif')
msgImg.add_header('Content-ID', '<giphy>')
msgImg.add_header('Content-Disposition', 'inline', filename="giphy.gif")


msg = MIMEMultipart()
msg['From'] = config.MAIL_FROM
msg['To'] = ", ".join(config.MAIL_TO)
msg['Subject'] = config.MAIL_SUBJECT


mailbody = open(config.MAIL_MESSAGE_PATH, 'rb').read()



messageHTML = MIMEText(mailbody,'plain', 'utf-8')
msg.attach(messageHTML)
msg.attach(msgImg)
mailserver = smtplib.SMTP(config.MAIL_SMTP_SERVER)
mailserver.ehlo()
mailserver.sendmail(config.MAIL_FROM, config.MAIL_TO, msg.as_string())
mailserver.quit()
