from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr, make_msgid, formatdate
import my_config
import my_p
import smtplib
import uuid

smtp_server = 'smtp.139.com'
smtp_server = 'smtp.qq.com'
smtp_port = 465
#smtp_port = 25
from_email = 'iinux@139.com'
from_email = 'iinux@qq.com'
to_email = ['iinux@139.com']
to_email = 'iinux@139.com'
to_email = 'iinux@qq.com'
password = my_p.password

def send2(content):
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = '邮件主题'  # 必须添加主题
    msg['Message-ID'] = '<unique-id@example.com>'  # 唯一标识

    # 添加邮件正文
    body = MIMEText(content, 'plain', 'utf-8')
    msg.attach(body)

    # 发送邮件
    my_email = smtplib.SMTP(smtp_server, smtp_port)
    my_email.starttls()
    my_email.login(from_email, password)
    my_email.sendmail(from_email, to_email, msg.as_string())
    my_email.quit()


def send3(content, subject='通知邮件'):
    # 配置信息
    from_name = '发件人名称'  # 添加发件人显示名称
    to_name = '收件人名称'

    try:
        # 创建邮件
        msg = MIMEMultipart('alternative')
        msg['From'] = formataddr((from_name, from_email))
        msg['To'] = formataddr((to_name, to_email))
        msg['Subject'] = subject
        msg['Message-ID'] = make_msgid()
        msg['X-Mailer'] = 'Python SMTP'

        # 邮件正文（同时添加纯文本和HTML版本）
        text_part = MIMEText(content, 'plain', 'utf-8')
        html_part = MIMEText(f'<html><body>{content}</body></html>', 'html', 'utf-8')

        msg.attach(text_part)
        msg.attach(html_part)

        # 连接并发送
        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, [to_email], msg.as_string())

        print("邮件发送成功")

    except smtplib.SMTPDataError as e:
        print(f"邮件被拒绝: {e}")
        # 可能是内容被识别为垃圾邮件
    except Exception as e:
        print(f"发送失败: {e}")


def send(subject, body='body'):
    if my_config.debug:
        return
    my_email = smtplib.SMTP_SSL(smtp_server, smtp_port)
    my_email.login(from_email, password)

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = from_email
    msg['To'] = to_email
    #msg['From'] = Header(f'Alice <{from_email}>')
    #msg['To'] = Header(f'Bob <{to_email}>')
    msg['Subject'] = subject
    msg['Date'] = formatdate()
    msg['Message-ID'] = make_msgid()

    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg['Message-ID'] = make_msgid()

    # 添加邮件正文
    body = MIMEText(body, 'plain', 'utf-8')
    msg.attach(body)

    my_email.sendmail(from_email, to_email, msg.as_string())
    my_email.quit()


send('明天放假','端午节快乐')
