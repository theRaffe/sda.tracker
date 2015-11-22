import smtplib
import ConfigParser

__author__ = 'macbook'

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
            print "Successfully sent email: to=%s , subject=%s " % (message["To"], message["Subject"])
            conn.quit()
        except smtplib.SMTPException, e:
            print "Error: unable to send email: %s" % e.message