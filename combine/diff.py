# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import os
from os import path
import filecmp
import tempfile

class Diff:

    def __init__(self, oldpath=None, newpath=None):
        self.oldpath = oldpath
        self.newpath = newpath

        self.added_files = []
        self.modified_files = []
        self.removed_files = []

    def walk(self):
        oldfiles = []
        newfiles = []

        for root, dirs, files in os.walk(self.oldpath):
            relpath = path.relpath(root, self.oldpath)

            for filename in files:
                oldfiles.append(path.join(relpath, filename))

        for root, dirs, files in os.walk(self.newpath):
            relpath = path.relpath(root, self.newpath)

            for filename in files:
                newfiles.append(path.join(relpath, filename))

        unused, self.modified_files, self.removed_files = filecmp.cmpfiles(self.oldpath, self.newpath, oldfiles)
        unused, self.modified_files, self.added_files = filecmp.cmpfiles(self.oldpath, self.newpath, newfiles)

