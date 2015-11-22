from mmredes.com.sda.emailing.EmailTracker import EmailTracker
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

__author__ = 'macbook'
if __name__ == '__main__':
    print "start test EmailTracker"
    config_file='../board.cfg'
    email_tracker = EmailTracker(config_file)
    message = MIMEMultipart()
    message['To'] = 'rafe2004@gmail.com'
    message['Subject'] = 'Test sda tracker'
    message_body = 'This is the text message of DriverEmailTest'
    message.attach(MIMEText(message_body))

    email_tracker.sendEmail(message)