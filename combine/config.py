# Copyright (c) 2010 John Reese
# Licensed under the MIT license

from os import path
from ConfigParser import SafeConfigParser

Config = SafeConfigParser()
Config.read(path.join(path.dirname(__file__), "defaults.conf"))

