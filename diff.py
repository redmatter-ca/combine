# Copyright (c) 2010 John Reese
# Licensed under the MIT license

from combine import Diff

d = Diff()
d.generate_update("1", "examples/ver1", "2", "examples/ver2")

