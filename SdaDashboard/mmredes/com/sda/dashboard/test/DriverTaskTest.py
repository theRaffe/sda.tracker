from mmredes.com.sda.dashboard.management.TaskManager import TaskManager

__author__ = 'macbook'
if __name__ == '__main__':
    task_manager = TaskManager('../board.cfg')
    print task_manager._dict_label
    print "OK"