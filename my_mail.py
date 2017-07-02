import smtplib
import my_config
from email.mime.text import MIMEText

smtp_server = 'smtp.139.com'
smtp_port = 25
from_email = 'iinux@139.com'
from_email_password = 'leuwai'
to_email = 'iinux@139.com'


def send(content, body='body'):
    if my_config.debug:
        return
    my_email = smtplib.SMTP(smtp_server, smtp_port)
    my_email.login(from_email, from_email_password)

    msg = MIMEText(body, 'plain', 'utf-8')
    # msg = email.mime.text.MIMEText(content,_subtype='plain')
    msg['to'] = to_email
    msg['from'] = from_email
    msg['subject'] = content

    my_email.sendmail(from_email, [to_email], msg.as_string())
    my_email.quit()

