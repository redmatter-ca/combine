# Copyright (c) 2010 John Reese
# Licensed under the MIT license

from combine import Update

u = Update("1", "file:///tmp/combine/Linux/manifest/1.yaml")
u.apply("examples/ver1")

