# Copyright (c) 2010 John Reese
# Licensed under the MIT license

from combine import Diff

d = Diff(oldpath="/tmp/combine/old", newpath="/tmp/combine/new")
d.walk()
