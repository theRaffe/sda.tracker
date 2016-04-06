import time
import win32com.client
import pythoncom
import re

from mmredes.com.sda.utils.FileWriter import FileWriter


class CheckMailer:
    def __init__(self, filename="LOG1.txt", mailbox="Archive Rafael Briones", folderindex=1):
        self.f = FileWriter(filename)
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = self.outlook.GetDefaultFolder(win32com.client.constants.olFolderInbox)
        self.inbox = inbox

    def check(self):
        # ===============================================================================
        # for i in xrange(1,100):                           #Uncomment this section if index 3 does not work for you
        #     try:
        #         self.inbox = self.outlook.Folders(i)     # "6" refers to the index of inbox for Default User Mailbox
        #         print "%i %s" % (i,self.inbox)            # "3" refers to the index of inbox for Another user's mailbox
        #     except:
        #         print "%i does not work"%i
        # ===============================================================================
        restrict_criteria = "@SQL=\"urn:schemas:httpmail:read\" = 0 And \"urn:schemas:mailheader:subject\"  like '%QC_MAAB.Sistemas_TVI%'";
        print restrict_criteria
        # And [Subject] like '%QC_MAAB.Sistemas_TVI -
        self.f.pl(time.strftime("%H:%M:%S"))
        tot = 0
        all_messages = self.inbox.Items
        messages = all_messages.Restrict(restrict_criteria)
        message = messages.GetFirst()
        while message:
            self.f.pl(message.Subject)
            message = messages.GetNext()
            tot += 1
        self.f.pl("Total Messages found: %i" % tot)
        self.f.pl("-" * 80)
        self.f.flush()


if __name__ == "__main__":
    mail = CheckMailer()
    mail.check()
