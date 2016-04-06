class FileWriter(object):
    '''
    convenient file wrapper for writing to files
    '''


    def __init__(self, filename):
        '''
        Constructor
        '''
        self.file = open(filename, "w")

    def pl(self, a_string):
        str_uni = a_string.encode('utf-8')
        self.file.write(str_uni)
        self.file.write("\n")

    def flush(self):
        self.file.flush()