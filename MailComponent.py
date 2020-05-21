#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 12:58:02 2020

@author: mavroudo
"""
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailComponent:
    def __init__(self):
        self.port=465 # For ssl
        self.password="" #this will be read from the enviroment
        self.sender_email = "eestec.voting@gmail.com"
        self.smtp_server= "smtp.gmail.com"
        self.html_to_vote="""\
                <html>
                  <body>
                    <p>Hi,<br>
                       How are you?<br>
                       <a href="https://www.facebook.com/xaris.toellinikofrapedaki">Σε παρακολουθούμε</a> 
                    </p>
                  </body>
                </html>
                """
        self.html_hash="""\
                <html>
                  <body>
                    <p>Hi,<br>
                       How are you?<br>
                       <a href="https://www.facebook.com/xaris.toellinikofrapedaki">Σε παρακολουθούμε</a> 
                    </p>
                  </body>
                </html>
                """
        self.context = ssl.create_default_context()
                
    def sendVotingCode(self,url_voting,receiver_email):
        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = self.sender_email
        message["To"] = receiver_email
        html = MIMEText(self.html_to_vote, "html")
        message.attach(html)
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())
    
    def sendHashValue(self,hashCreated,receiver_email):
        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = self.sender_email
        message["To"] = receiver_email
        html = MIMEText(self.html_to_vote, "html")
        message.attach(html)
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())
        








# Turn these into plain/html MIMEText objects
#part1 = MIMEText(text, "plain")


# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
#message.attach(part1)


# Create a secure SSL context




