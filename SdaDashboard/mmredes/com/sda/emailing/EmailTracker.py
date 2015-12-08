import smtplib
import ConfigParser
import os

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

__author__ = 'macbook'

cwd = os.getcwd()
class EmailTracker:
    config_file = ''
    smtp_server = ''
    imap_server = ''
    email_account = ''
    email_password = ''
    smtp_port = 0

    def __init__(self, config_file):
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        self.config_file = config_file
        self.smtp_server = config.get('SettingEmail', 'smtp.server')
        self.imap_server = config.get('SettingEmail', 'imap.server')
        self.email_account = config.get('SettingEmail', 'email.account')
        self.email_password = config.get('SettingEmail', 'email.password')
        self.smtp_port = config.getint('SettingEmail', 'smtp.port')

    def sendEmail(self, message):
        try:
            receivers = message['To']
            message['From'] = self.email_account
            conn = smtplib.SMTP(self.smtp_server, self.smtp_port)
            conn.login(self.email_account, self.email_password)
            conn.sendmail(self.email_account, receivers, message.as_string())
            print "message email: %s" % message.as_string()
            print "Successfully sent email: to=%s , subject=%s " % (message["To"], message["Subject"])
            conn.quit()
        except smtplib.SMTPException, e:
            print "Error: unable to send email: %s" % e.message

    def get_email_ticket_request(self, dict_board_code):
        list_artifact = dict_board_code['artifacts']
        dict_board = dict_board_code['dict_board']
        id_ticket = dict_board['id_ticket']
        message = MIMEMultipart()
        list_email = []
        for dict_artifact in list_artifact:
            email_request = dict_artifact['user']
            list_email.append(email_request)

        config = ConfigParser.RawConfigParser()
        config.read(self.config_file)
        subject = config.get('SettingEmail', 'subject.request.ticket')
        code_env = dict_board['code_environment']
        subject = subject % (id_ticket, code_env)
        message['Subject'] = subject
        message['To'] = ','.join(list_email)

        file_template_email = os.path.join(cwd, 'res/template/request_ticket_email.html')
        file_email = open(file_template_email, 'r')
        body_message = file_email.read()
        body_message = body_message % id_ticket
        message.attach(MIMEText(body_message))

        return message
