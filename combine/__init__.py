# Copyright (c) 2010 John Reese
# Licensed under the MIT license

class CombineError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

from combine.hash import sha1
from combine.formats import Archive, File
from combine.config import Config
from combine.package import Package
from combine.manifest import Manifest
from combine.uri import URI

from combine.diff import Diff

