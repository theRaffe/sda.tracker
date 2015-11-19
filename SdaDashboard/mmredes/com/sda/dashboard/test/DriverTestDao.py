import ConfigParser
from mmredes.com.sda.dashboard.dao.SdaTrackerDao import SdaTrackerDao

__author__ = 'macbook'
if __name__ == '__main__':
    print "start test dao"
    config_file='../board.cfg'
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    print ("sections", config.sections())
    connection_file = config.get('DatabaseSection', 'database.file')
    driverDao = SdaTrackerDao(connection_file)
    row = driverDao.get_ticket_board_code("feature2")
    print row

    rows = driverDao.get_artifact_code("feature2")
    print rows
