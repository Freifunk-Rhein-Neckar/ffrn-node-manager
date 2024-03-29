import configparser
import smtplib
from email.mime.text import MIMEText
import email.utils

def sendemail(message, receivers):
    config = configparser.ConfigParser()
    config.read('settings.conf')
    smtp_host = config['SMTP']['host']
    smtp_port = config['SMTP'].getint('port')
    smtp_user = config['SMTP']['user']
    smtp_pass = config['SMTP']['pass']
    mail_from = config['MAIL']['from']
    mail_bcc = config['MAIL'].get('bcc',"")
    smtp_starttls = config['SMTP'].getboolean('starttls')

    if not message['From']:
        message['From'] = mail_from

    if not message['Message-ID']:
        message['Message-ID'] = email.utils.make_msgid()

    if not message['Date']:
        message['Date'] = email.utils.formatdate()

    if mail_bcc:
        receivers = [receivers] + [mail_bcc]

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.set_debuglevel(False)

        if smtp_starttls:
            server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(mail_from, receivers, message.as_string())


if __name__ ==  "__main__":

    sub = input("Subject: ")
    msg = input("Message: ")
    to = input("Recipient: ")
    replyTo = input("Reply-To: ")

    message = MIMEText(msg)
    message['Subject'] = sub
    message['Reply-To'] = replyTo

    sendemail(message, [to])