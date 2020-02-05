import configparser
import smtplib
from email.mime.text import MIMEText

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

    message = MIMEText(msg)
    message['Subject'] = sub

    sendemail(message, [to])