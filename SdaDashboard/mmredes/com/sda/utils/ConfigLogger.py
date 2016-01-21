import logging
import logging.config
from pkg_resources import resource_filename


def get_sda_logger():
    config_file = resource_filename('mmredes.com.sda.utils', 'logging.conf')
    # print "config_file_log = %s" % config_file
    logging.config.fileConfig(config_file)
