#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 12:58:02 2020

@author: mavroudo
"""
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailComponent:
    def __init__(self, sender_email, password, smtp_server, port):
        self.port = port  # For ssl
        self.password = password
        self.sender_email = sender_email
        self.smtp_server = smtp_server
        self.html_to_vote = """\
                <html>
                  <body>
                    <p>Hi,<br>
                       How are you?<br>
                       <a href="https://www.facebook.com/xaris.toellinikofrapedaki">Σε παρακολουθούμε</a> 
                    </p>
                  </body>
                </html>
                """
        self.html_hash = """\
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
        message["Subject"] = "Vote in EESTEC"
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
        





import os
if __name__ == '__main__':
    mail = os.getenv("MAIL_ACCOUNT")
    password = os.getenv("MAIL_PASSWORD")
    smtp_server=os.getenv("MAIL_SMTP_SERVER")
    port=os.getenv("MAIL_SMTP_PORT")
    print(mail,password,smtp_server,port)

# Turn these into plain/html MIMEText objects
#part1 = MIMEText(text, "plain")


# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
#message.attach(part1)


# Create a secure SSL context




