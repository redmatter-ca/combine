
from os import path
from ConfigParser import SafeConfigParser

Config = SafeConfigParser()
Config.read(path.join(path.dirname(__file__), "defaults.conf"))

