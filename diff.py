# Copyright (c) 2010 John Reese
# Licensed under the MIT license

from combine import Diff

d = Diff(oldpath="/tmp/cb/old", newpath="/tmp/cb/new", outputpath="/tmp/cb/out")
d.walk()
