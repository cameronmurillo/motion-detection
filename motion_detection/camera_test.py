import cv2
import numpy as np
import smtplib, ssl
import os
import imghdr
import time
from email.message import EmailMessage
from decouple import config

EMAIL_ADDRESS = "cameronmurillo@gmail.com"
EMAIL_PASSWORD = "Alex2177"

#setup email information to send
msg = EmailMessage()
msg['Subject'] = 'Motion Detector'
msg['From'] = "cameronmurillo@gmail.com"
msg['To'] = "camurillo@ucdavis.edu"
msg.set_content("There has been motion detected at this time. Please see image.")


#Gets camera access
cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
ret, frame2 = cap.read()
with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
	smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
	while cap.isOpened():
		# subtract the 2nd frame and first frame to find difference
		diff = cv2.absdiff(frame1, frame2)
		# convert colored image (the difference) to gray
		gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
		# blurs the gray iamge
		blur = cv2.GaussianBlur(gray, (5,5), 0)
		_, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
		dilated = cv2.dilate(thresh, None, iterations = 3)
		contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		for contour in contours:
			(x, y, w, h) = cv2.boundingRect(contour)

			#ignore, dont draw rectangle
			if cv2.contourArea(contour) < 20000:
				continue
			cv2.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 2)
			cv2.putText(frame1, "Status: {}".format('Movement'), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

			#take screenshot 
			cv2.imwrite("who_moved/pic_copy.jpg", frame1)
			# 
			with open("who_moved/pic_copy.jpg",'rb') as f:
				file_data = f.read()
				file_type = imghdr.what(f.name)
				file_name = f.name
			msg.add_attachment(file_data,maintype ='image', subtype=file_type,filename=file_name)
			smtp.send_message(msg)
		
		#show feed
		cv2.imshow("feed",frame1)

		# gather new frame to find difference between the previous frame
		frame1 = frame2
		ret, frame2 = cap.read()
		# ESC key to break out
		if cv2.waitKey(40) == 27:
			break

cv2.destroyAllWindows()
cap.release()