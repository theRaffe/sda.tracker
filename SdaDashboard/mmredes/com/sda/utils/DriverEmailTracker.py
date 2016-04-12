import ConfigParser
import time
import win32com.client
import pythoncom
import re

from mmredes.com.sda.emailing.EmailTracker import process_defect_email
from mmredes.com.sda.utils.FileWriter import FileWriter


class DriverEmailTracker:
    def __init__(self, filename="LOG1.txt", host_port=""):
        # mailbox="Archive Rafael Briones", folderindex=1):
        self.f = FileWriter(filename)
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = self.outlook.GetDefaultFolder(win32com.client.constants.olFolderInbox)
        self.inbox = inbox
        self.host_port = host_port

    def check(self):
        restrict_criteria = "@SQL=\"urn:schemas:httpmail:read\" = 0 And \"urn:schemas:mailheader:subject\"  like 'QC_MAAB.Sistemas_TVI%'";
        print restrict_criteria
        # And [Subject] like '%QC_MAAB.Sistemas_TVI -
        self.f.pl(time.strftime("%H:%M:%S"))
        tot = 0
        all_messages = self.inbox.Items
        messages = all_messages.Restrict(restrict_criteria)
        message = messages.GetFirst()
        while message:
            print message.Subject
            self.f.pl(message.Subject)
            self.f.pl(message.HTMLBody)
            process_defect_email(message.HTMLBody, self.host_port)
            message = messages.GetNext()
            tot += 1
        self.f.pl("Total Messages found: %i" % tot)
        self.f.pl("-" * 80)
        self.f.flush()


if __name__ == "__main__":
    config_parser = ConfigParser.RawConfigParser()
    config_parser.read('emailSdaTracker.cfg')
    host_web_server = config_parser.get('SettingEmail', 'host.web.server')
    port_web_server = config_parser.get('SettingEmail', 'port.web.server')
    mailBox = config_parser.get('SettingEmail', 'mailBox')
    folderIndex = config_parser.get('SettingEmail', 'folderIndex')
    hos_port = '%s:%s' % (host_web_server, port_web_server)
    mail = DriverEmailTracker(host_port=hos_port)
    mail.check()
