# Copyright (c) 2010 John Reese
# Licensed under the MIT license

class PrepError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

from combine.diff import Diff

