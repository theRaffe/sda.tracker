import logging
import smtplib
import ConfigParser
import os
import imaplib
import email

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from mmredes.com.sda.dashboard.PersistentController import PersistentController
from mmredes.com.sda.emailing.EmailParser import EmailParser
from pkg_resources import resource_filename

__author__ = 'macbook'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

dir_path = os.path.dirname(__file__)


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

    def send_email(self, message):
        try:
            receivers = message['To']
            message['From'] = self.email_account
            conn = smtplib.SMTP(self.smtp_server, self.smtp_port)
            conn.login(self.email_account, self.email_password)
            conn.sendmail(self.email_account, receivers, message.as_string())
            logger.debug("message email: %s" % message.as_string())
            logger.info("Successfully sent email: to=%s , subject=%s " % (message["To"], message["Subject"]))
            conn.quit()
        except smtplib.SMTPException as e:
            logger.warning("Error, unable to send email: %s" % e.message)
        except RuntimeError as e:
            logger.warning("Unexpected error has occurred: %s" % e.message)

    def get_email_ticket_request(self, dict_board_code):
        list_artifact = dict_board_code['artifacts']
        ticket_board_code = dict_board_code['dict_board']
        logger.info(ticket_board_code)

        id_ticket = ticket_board_code.ticket_board.id_ticket
        message = MIMEMultipart()
        list_email = []
        for ticket_artifact_code in list_artifact:
            email_request = ticket_artifact_code.ticket_artifact.modification_user
            list_email.append(email_request)

        config = ConfigParser.RawConfigParser()
        config.read(self.config_file)
        subject = config.get('SettingEmail', 'subject.request.ticket')
        code_env = ticket_board_code.cat_environment.code_environment
        subject = subject % (id_ticket, code_env)
        message['Subject'] = subject
        message['To'] = ','.join(list_email)

        list_tech = set(m_ticket_artifact.cat_type_tech.code_type_tech for m_ticket_artifact in list_artifact)

        file_template_email = resource_filename('mmredes.com.sda.dashboard.resource.template',
                                                'request_ticket_email.html')
        file_template_row = resource_filename('mmredes.com.sda.dashboard.resource.template',
                                              'ticket_row.html')
        file_email = open(file_template_email, 'r')
        file_ticket_row = open(file_template_row, 'r')

        body_message = file_email.read()
        body_message = body_message.replace('@id_ticket@', id_ticket)

        row_ticket = file_ticket_row.read()
        rows_ticket = ''
        for code_tech in list_tech:
            row_text = row_ticket.replace('@code_tech@', code_tech)
            row_text = row_text.replace('@id_ticket@', id_ticket)
            row_text = row_text.replace('@path_release@', '\\searchlight\sda\%s\%s' % (id_ticket, code_tech))
            rows_ticket += row_text
        body_message = body_message.replace('@rows_ticket@', rows_ticket)

        message.attach(MIMEText(body_message, 'html'))
        logger.info(body_message)
        return message

    def listen_email(self):
        persistent_controller = PersistentController(self.config_file)
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
            email_message = self.get_decoded_email_body(raw_body)
            # print ("result: %s" % result)
            # print ("body_email: %s" % email_message)
            dict_defect = email_parser.parse_mail_defect(email_message)
            if dict_defect:
                logger.info("dict_defect: %s" % dict_defect)
                persistent_controller.process_library_ticket(dict_defect)

    @staticmethod
    def get_decoded_email_body(message_body):
        """ Decode email body.
        Detect character set if the header is not set.
        We try to get text/plain, but if there is not one then fallback to text/html.
        :param message_body: Raw 7-bit message body input e.g. from imaplib. Double encoded in quoted-printable and latin-1
        :return: Message body as unicode string
        """
        msg = email.message_from_string(message_body)
        text = ""
        if msg.is_multipart():
            html = None
            for part in msg.get_payload():

                print "%s, %s" % (part.get_content_type(), part.get_content_charset())

                if part.get_content_charset() is None:
                    # We cannot know the character set, so return decoded "something"
                    text = part.get_payload(decode=True)
                    continue

                charset = part.get_content_charset()

                if part.get_content_type() == 'text/plain':
                    text = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')

                if part.get_content_type() == 'text/html':
                    html = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')

            if html is not None:
                return html.strip()
                # else:
                #    return text.strip()
        else:
            text = unicode(msg.get_payload(decode=True), msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
            return text.strip()
