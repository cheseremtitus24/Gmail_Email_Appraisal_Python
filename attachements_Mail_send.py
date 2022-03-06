# to query:
import sys
import ast
from datetime import datetime

import smtplib
import mimetypes
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

from dotenv import load_dotenv, dotenv_values

load_dotenv()  # take environment variables from .env.

import smtplib

tls_port = 587
ssl_port = 465
smtp_server_domain_names = {'GMAIL': ('smtp.gmail.com', tls_port, ssl_port),
                            'OUTLOOK': ('smtp-mail.outlook.com', tls_port, ssl_port),
                            'YAHOO': ('smtp.mail.yahoo.com', tls_port, ssl_port),
                            'AT&T': ('smtp.mail.att.net', tls_port, ssl_port),
                            }


# todo: Ability to choose mail server provider
# auto read in from the dictionary the respective mail server address and the tls and ssl ports

class Bimail:
    def __init__(self, subject, recipients):
        self.subject = subject
        self.recipients = recipients
        self.htmlbody = ''
        self.sender = "cheseremtitus4@gmail.com"
        self.senderpass = 'gnhfpsjmlnzribhk'
        self.attachments = []

    # Creating an smtp object
    # todo: if gmail passed in use gmail's dictionary values

    def setup_mail_client(self, domain_key_to_use="GMAIL",
                          email_servers_domains_dict=smtp_server_domain_names):
        """

        :param report_pdf:
        :type to_address: str
        """
        smtpObj = None
        encryption_status = True
        config = dotenv_values(".env")
        # check if the domain_key exists from within the available email-servers-domains dict file passed in
        # else throw an error

        # read environment file to get the Domain to be used
        if f"{domain_key_to_use}" in email_servers_domains_dict.keys():
            # if the key is found do the following
            # 1.extract the domain,tls,ssl ports from email_servers dict for use in program
            try:
                values_tuple = email_servers_domains_dict.get(f"{domain_key_to_use}")
                ssl_port = values_tuple[2]
                tls_port = values_tuple[1]
                smtp_server = values_tuple[0]
                try:
                    smtpObj = smtplib.SMTP_SSL(smtp_server, ssl_port)
                    print(f"Success connect with ssl on {ssl_port}")
                    encryption_status = True
                except:
                    print(f"Failed connection via ssl on port {ssl_port}")


            except:
                print(f"Failed connection via ssl on port {ssl_port}")
                try:
                    smtpObj = smtplib.SMTP(smtp_server, tls_port)
                    print(f"Success connect with tls on {tls_port}")
                    print('Awaiting for connection encryption via startttls()')
                except:
                    pass
                encryption_status = False
            finally:
                print("Within Finally block")
                if not smtpObj:
                    print("Failed!!!  no Internet connection")
                else:
                    # if connection channel is unencrypted via the use of tls encrypt it
                    if not encryption_status:
                        status = smtpObj.starttls()
                        if status[0] == 220:
                            print("Successfully Encrypted tls channel")

                    print("Successfully Connected!!!! Requesting Login")
                    # Loading .env file values to config variable

                    status = smtpObj.login(f'{config.get("EMAIL")}', f'{config.get("SECRET_KEY")}')
                    # status = smtpObj.login('cheseremtitus24@gmail.com','EstherMutiso')
                    if status[0] == 235:
                        print("Successfully Authenticated User to xxx account")
                        success = self.send(smtpObj, f'{config.get("EMAIL")}')
                        if not bool(success):
                            print(f"Success in Sending Mail to  {success}")
                            print("Disconnecting from Server INstance")
                            quit_result = smtpObj.quit()

                        else:
                            print(f"Failed to Post {success}!!!")
                            print(f"Quiting anyway !!!")
                            quit_result = smtpObj.quit()
                    else:
                        print("Application Specific Password is Required")
        else:

            print("World")

    def send(self,smtpObj,from_address):
        msg = MIMEMultipart('alternative')
        msg['From'] = from_address
        msg['Subject'] = self.subject
        msg['To'] = ", ".join(self.recipients)  # to must be array of the form ['mailsender135@gmail.com']
        msg.preamble = "preamble goes here"
        # check if there are attachments if yes, add them
        if self.attachments:
            self.attach(msg)
        # add html body after attachments
        msg.attach(MIMEText(self.htmlbody, 'html'))
        # send
        print(f"Attempting Email send to the following addresses {self.recipients}")
        result = smtpObj.sendmail(from_address, self.recipients,msg.as_string())
        return result
        # s = smtplib.SMTP('smtp.gmail.com:587')
        # s.starttls()
        # s.login(self.sender, self.senderpass)
        # s.sendmail(self.sender, self.recipients, msg.as_string())
        # test
        # print(msg)
        # s.quit()

    def htmladd(self, html):
        self.htmlbody = self.htmlbody + '<p></p>' + html

    def attach(self, msg):
        for f in self.attachments:

            ctype, encoding = mimetypes.guess_type(f)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)

            if maintype == "text":
                fp = open(f)
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "image":
                fp = open(f, "rb")
                attachment = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()

            elif maintype == "ppt":
                fp = open(f, "rb")
                attachment = MIMEApplication(fp.read(), _subtype=subtype)
                fp.close()

            elif maintype == "audio":
                fp = open(f, "rb")
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(f, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=f)
            attachment.add_header('Content-ID', '<{}>'.format(f))
            msg.attach(attachment)

    def addattach(self, files):
        self.attachments = self.attachments + files


# example below
if __name__ == '__main__':
    # subject and recipients
    mymail = Bimail('Sales email ' + datetime.now().strftime('%Y/%m/%d'),['cheseremtitus@yahoo.com'])
                    #['support@bmtechsys.com'])
    # start html body. Here we add a greeting.
    mymail.htmladd('Good morning, find the daily summary below.')
    # Further things added to body are separated by a paragraph, so you do not need to worry about newlines for new sentences
    # here we add a line of text and an html table previously stored in the variable
    mymail.htmladd('Daily sales')
    mymail.addattach(['htmlsalestable.xlsx'])
    # another table name + table
    mymail.htmladd('Daily bestsellers')
    mymail.addattach(['htmlbestsellertable.xlsx'])
    # add image chart title
    mymail.htmladd('Weekly sales chart')
    # attach image chart
    mymail.addattach(['saleschartweekly.png'])
    # refer to image chart in html
    mymail.htmladd('<img src="cid:saleschartweekly.png"/>')
    # attach another file
    mymail.addattach(['MailSend.py'])
    # send!
    # mymail.send()
    mymail.setup_mail_client( domain_key_to_use="GMAIL",email_servers_domains_dict=smtp_server_domain_names)