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

def send_appraissal_email(smtpObj, from_address, to_address):
    ''''
    sends emails to list of strings of emails
    returns a dictionary with a list of failed send recipients
    '''
    print(f"Attempting Email send to the following addresses {to_address}")
    result = smtpObj.sendmail(from_address, to_address,
                              'Subject: Check for Errors.\nDear Alice, Multiple Recepients. Sincerely,Bob')
    return result


# Creating an smtp object
# todo: if gmail passed in use gmail's dictionary values

def setup_mail_client(to_address, report_pdf=None, domain_key_to_use="GMAIL", email_servers_domains_dict=smtp_server_domain_names):
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
        #if the key is found do the following
        #1.extract the domain,tls,ssl ports from email_servers dict for use in program
        try:
            values_tuple = email_servers_domains_dict.get(f"{domain_key_to_use}")
            ssl_port = values_tuple[2]
            tls_port = values_tuple[1]
            smtp_server = values_tuple[0]

            smtpObj = smtplib.SMTP(smtp_server, tls_port)
            print(f"Success connect with tls on {tls_port}")
            print('Awaiting for connection encryption via startttls()')
            encryption_status = False

        except:
            print(f"Failed connection via tls on port {tls_port}")
            try:
                smtpObj = smtplib.SMTP_SSL(smtp_server, ssl_port)
                print(f"Success connect with ssl on {ssl_port}")
                encryption_status = True
            except:
                print(f"Failed connection via ssl on port {ssl_port}")
        finally:
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
                    success = send_appraissal_email(smtpObj, f'{config.get("EMAIL")}',
                                                    [f'{to_address}'])
                    if not bool(success):
                        print(f"Success in Sending Mail to  {success}")
                        print("Disconnecting from Server INstance")
                        quit_result = smtpObj.quit()

                    else:
                        print(f"Failed to Post {success}!!!")
                else:
                    print("Application Specific Password is Required")
    else:

        print("World")



print(smtp_server_domain_names.keys())
# print(type(smtpObj))
