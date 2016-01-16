import logging
import logging.config
import os


def get_sda_logger(name_logger):
    dir_path = os.path.dirname(__file__)
    config_file = os.path.join(dir_path, 'logging.conf')

    print "config_file: %s" % config_file
    logging.config.fileConfig(config_file)
    return logging.getLogger(name_logger)
