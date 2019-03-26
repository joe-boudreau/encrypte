import os
from configparser import ConfigParser

config = ConfigParser()
config.read("../config.properties")


def get_data_directory():
    """
    Returns the directory where all the user data should be stored
    :return: Absolute directory path to user data directory
    :rtype string
    """
    root_directory = os.path.realpath('..')  # the data directory is relative to the root project directory
    return root_directory + '/' + config['main']['user.data.directory']


def get_encryption_seed():
    """
    Returns the seed/IV value used for all encryption operations
    :return: seed value as a string
    :rtype string
    """
    return config['main']['encryption.seed.value']
