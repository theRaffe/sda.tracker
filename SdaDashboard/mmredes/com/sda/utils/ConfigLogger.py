import logging
import logging.config
import os


def get_sda_logger():
    dir_path = os.path.dirname(__file__)
    config_file = os.path.join(dir_path, 'logging.conf')

    logging.config.fileConfig(config_file)
