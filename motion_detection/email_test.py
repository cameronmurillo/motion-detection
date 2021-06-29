import cv2
import numpy as np
import smtplib, ssl
import os
from email.message import EmailMessage
import imghdr

#rec_email ="joselle2001@gmail.com"
#sender_email = "cameronmurillo@gmail.com"
#password = "Alex2177"
#message = "Motion Detected"
#server = smtplib.SMTP('smtp.gmail.com', 587)
#server.starttls()
#print('trying to login')
#server.login(sender_email,password)
#print("Login Success")
#server.sendmail(sender_email,rec_email,message)
#print("email has been sent")
EMAIL_ADDRESS = "cameronmurillo@gmail.com"
EMAIL_PASSWORD = "Alex2177"


msg = EmailMessage()
msg['Subject'] = 'Motion Detector'
msg['From'] = "cameronmurillo@gmail.com"
msg['To'] = "camurillo@ucdavis.edu"
msg.set_content("There has been motion detected at this time. Please see image")
with open("who_moved/pic_copy.jpg",'rb') as f:
	file_data = f.read()
	file_type = imghdr.what(f.name)
	file_name = f.name

msg.add_attachment(file_data,maintype ='image', subtype=file_type,filename=file_name)
with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
	smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
	smtp.send_message(msg)
	print('made it here')
