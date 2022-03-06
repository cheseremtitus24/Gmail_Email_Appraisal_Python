def send_email_pdf_figs(path_to_pdf, subject, message, destination, password_path=None):
    ## credits: http://linuxcursor.com/python-programming/06-how-to-send-pdf-ppt-attachment-with-html-body-in-python-script
    from socket import gethostname
    #import email
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib
    import json

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    with open(password_path) as f:
        config = json.load(f)
        server.login('me@gmail.com', config['password'])
        # Craft message (obj)
        msg = MIMEMultipart()

        message = f'{message}\nSend from Hostname: {gethostname()}'
        msg['Subject'] = subject
        msg['From'] = 'me@gmail.com'
        msg['To'] = destination
        # Insert the text to the msg going by e-mail
        msg.attach(MIMEText(message, "plain"))
        # Attach the pdf to the msg going by e-mail
        with open(path_to_pdf, "rb") as f:
            #attach = email.mime.application.MIMEApplication(f.read(),_subtype="pdf")
            attach = MIMEApplication(f.read(),_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename=str(path_to_pdf))
        msg.attach(attach)
        # send msg
        server.send_message(msg)
