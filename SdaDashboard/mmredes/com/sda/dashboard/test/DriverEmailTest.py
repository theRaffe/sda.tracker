import unittest

from mmredes.com.sda.emailing.EmailTracker import EmailTracker
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

__author__ = 'macbook'


class DriverEmailTest(unittest.TestCase):
    def test01_send_mail(self):
        print "start test EmailTracker"
        config_file = '../board.cfg'
        email_tracker = EmailTracker(config_file)

        dict_board = {"id_ticket": "T100","code_environment": "QA2"}
        artifacts = [
            {"artifact": "cartridge-1", "tech": "java", "user": "rafe2004@gmail.com"},
            {"artifact": "cartridge-2", "tech": "java", "user": "rafe2004@gmail.com"},
            {"artifact": "mediator", "tech": "osb", "user": "rafe2004@gmail.com"}]
        dict_board_code = {"dict_board": dict_board, "artifacts": artifacts}
        print dict_board_code
        message = MIMEMultipart()
        message['To'] = 'rafe2004@gmail.com'
        message['Subject'] = 'Test sda tracker'
        message_body = 'This is the text message of DriverEmailTest'
        message.attach(MIMEText(message_body))

        message = email_tracker.get_email_ticket_request(dict_board_code)

        email_tracker.send_email(message)
        self.assertTrue(True)

    def test02_listen_new(self):
        config_file = '../board.cfg'
        email_tracker = EmailTracker(config_file)
        email_tracker.listen_email()


if __name__ == '__main__':
    unittest.main()
