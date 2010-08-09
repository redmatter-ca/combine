# Copyright (c) 2010 John Reese
# Licensed under the MIT license

from combine import Diff, Config

Config.read("test.conf")
d = Diff()
d.generate_update("1", "ver1", "2", "ver2")

