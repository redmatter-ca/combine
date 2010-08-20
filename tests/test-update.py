# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

from combine import Update

u = Update("1", "file:///tmp/combine/Linux/manifest/1.yaml")
u.apply("ver1")

