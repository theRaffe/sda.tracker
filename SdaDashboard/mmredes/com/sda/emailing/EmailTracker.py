import smtplib
import ConfigParser
import os
import imaplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from mmredes.com.sda.emailing.EmailParser import EmailParser

__author__ = 'macbook'

cwd = os.getcwd()
class EmailTracker:
    config_file = ''
    smtp_server = ''
    imap_server = ''
    email_account = ''
    email_password = ''
    smtp_port = 0
    config = None

    def __init__(self, config_file):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)
        self.config_file = config_file
        self.smtp_server = self.config.get('SettingEmail', 'smtp.server')
        self.imap_server = self.config.get('SettingEmail', 'imap.server')
        self.email_account = self.config.get('SettingEmail', 'email.account')
        self.email_password = self.config.get('SettingEmail', 'email.password')
        self.smtp_port = self.config.getint('SettingEmail', 'smtp.port')


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

    def listen_email(self):
        mail = imaplib.IMAP4_SSL(self.imap_server)
        mail.login(self.email_account, self.email_password)
        mail.list()
        mail.select('inbox')
        email_parser = EmailParser()

        subject_defect = self.config.get('SettingEmail', 'subject.defect')
        substring_start = self.config.get('SettingEmail', 'substring.to.start')
        typ, data = mail.search(None, '(UNSEEN SUBJECT "%s")' % subject_defect)
        messages = data[0].split()
        for message_uid in messages:
            result, data = mail.uid('fetch', message_uid, '(RFC822)')
            raw_body = data[0][1]
            start_index = raw_body.find(substring_start)
            body_email = raw_body[start_index: len(raw_body)]
            print ("result: %s" % result)
            print ("body_email: %s" % body_email)
            dict_defect = email_parser.parse_mail_defect(body_email)

            print("dict_defect: %s" % dict_defect)
