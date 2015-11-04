__author__ = 'macbook'
from mmredes.com.sda.dashboard.dao.SdaTrackerDao import SdaTrackerDao

class DriverDao:
    dao_object = None
    connection_file = '/Users/macbook/Documents/workspaces/python/sda_tracker_workspace/sda.tracker/db.sda.tracker/sda_tracking.db'

    def __init__(self):
        self.dao_object = SdaTrackerDao(self.connection_file)

    def get_artifacts(self):
        return self.dao_object.get_artifacts()

driver = DriverDao()
print driver.get_artifacts()