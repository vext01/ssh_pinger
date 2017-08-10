#!/usr/bin/env python2.7

import socket
import time
import datetime

# XXX needs a config file
HOST = "your hostname here"
PORT = 22
POLL_INTVL = 60 * 15
MAIL_TO = ["your-email-addresses-here"]


def check_host(hostname):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        r = s.connect((hostname, PORT))
    except Exception as e:
        return str(e)
    finally:
        s.close()


def send_mail(msg):
    import smtplib
    from email.mime.text import MIMEText
    import subprocess

    subject = '%s status' % HOST

    mail = MIMEText(msg)
    mail['Subject'] = subject
    mail['From'] = 'edd'
    mail['To'] = ", ".join(MAIL_TO)

    args = ["mail", "-s", subject] + MAIL_TO
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    _, serr = p.communicate(str(mail))
    if p.returncode != 0:
        print("failed to send mail: %s" % serr)
    else:
        print("Mail sent")


def loop():
    last_status_up = True
    while(True):
        date_s = str(datetime.datetime.now())
        exn_str = check_host(HOST)
        if exn_str is not None:
            msg = "%s: %s is DOWN!" % (date_s, HOST)
            if last_status_up:
                send_mail(msg)
            last_status_up = False
        else:
            msg = "%s: %s is UP" % (date_s, HOST)
            if not last_status_up:
                send_mail(msg)
            last_status_up = True
        print(msg)
        time.sleep(POLL_INTVL)

if __name__ == "__main__":
    loop()
