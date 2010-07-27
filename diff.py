# Copyright (c) 2010 John Reese
# Licensed under the MIT license

from combine import Diff, Manifest, Change

#d = Diff(oldpath="/tmp/combine/old", newpath="/tmp/combine/new")
#d.walk()

m = Manifest(1,3)
m.add_change(Change("create", "bar"))
m.add_change(Change("replace", "foo"))

str = m.to_yaml()
print str

m2 = Manifest.from_yaml(str)
print m2.to_yaml()
