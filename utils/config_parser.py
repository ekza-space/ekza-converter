import configparser
from os import path
from settings import ROOT_DIR

config = configparser.ConfigParser()
config.sections()

config_file = path.join(ROOT_DIR, 'config.ini')
config.read(config_file)

CONVERTER = config['PATH']['CONVERTER']
POST_URL = config['API']['POST_URL']
