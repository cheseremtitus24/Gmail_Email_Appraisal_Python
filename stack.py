import smtplib, ssl
from os.path import basename
from email.mime.base import MIMEBase
from mimetypes import guess_type
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.charset import Charset


def try_coerce_ascii(string_utf8):
    """Attempts to decode the given utf8-encoded string
       as ASCII after coercing it to UTF-8, then return
       the confirmed 7-bit ASCII string.

       If the process fails (because the string
       contains non-ASCII characters) returns ``None``.
    """
    try:
        string_utf8.encode('ascii')
    except UnicodeEncodeError:
        return
    return string_utf8


def encode_header_param(param_text):
    """Returns an appropriate RFC 2047 encoded representation of the given
       header parameter value, suitable for direct assignation as the
       param value (e.g. via Message.set_param() or Message.add_header())
       RFC 2822 assumes that headers contain only 7-bit characters,
       so we ensure it is the case, using RFC 2047 encoding when needed.

       :param param_text: unicode or utf-8 encoded string with header value
       :rtype: string
       :return: if ``param_text`` represents a plain ASCII string,
                return the same 7-bit string, otherwise returns an
                ASCII string containing the RFC2047 encoded text.
    """
    if not param_text: return ""
    param_text_ascii = try_coerce_ascii(param_text)
    return param_text_ascii if param_text_ascii \
        else Charset('utf8').header_encode(param_text)


smtp_server = '<someserver.com>'
smtp_port = 465  # Default port for SSL
sender_email = '<sender_email@some.com>'
sender_password = '<PASSWORD>'
receiver_emails = ['<receiver_email_1@some.com>', '<receiver_email_2@some.com>']
subject = 'Test message'
message = """\
Hello! This is a test message with attachments.

This message is sent from Python."""

files = ['<path1>/файл1.pdf', '<path2>/файл2.png']

# Create a secure SSL context
context = ssl.create_default_context()

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = COMMASPACE.join(receiver_emails)
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = subject

msg.attach(MIMEText(message))

for f in files:
    mimetype, _ = guess_type(f)
    mimetype = mimetype.split('/', 1)
    with open(f, "rb") as fil:
        part = MIMEBase(mimetype[0], mimetype[1])
        part.set_payload(fil.read())
        encode_base64(part)
    filename_rfc2047 = encode_header_param(basename(f))

    # The default RFC 2231 encoding of Message.add_header() works in Thunderbird but not GMail
    # so we fix it by using RFC 2047 encoding for the filename instead.
    part.set_param('name', filename_rfc2047)
    part.add_header('Content-Disposition', 'attachment', filename=filename_rfc2047)
    msg.attach(part)

with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_emails, msg.as_string())
