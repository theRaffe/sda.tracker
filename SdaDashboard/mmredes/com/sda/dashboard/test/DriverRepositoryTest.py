import unittest
import logging

from mmredes.com.sda.dashboard.repository.RepositoryListener import RepositoryListener

__author__ = 'macbook'
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DriverRepositoryTest(unittest.TestCase):
    def test01_get_branch(self):
        config_file = '../board.cfg'
        repository_listener = RepositoryListener(config_file)
        branch = repository_listener.get_current_branch()
        logger.info('branch detected: %s' % branch)
        self.assertEqual(branch, 'develop', 'Error current branch is incorrect: %s' % branch)
