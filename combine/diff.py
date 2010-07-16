# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import os
from os import path
import tempfile

class Diff:

    def __init__(self, oldpath=None, newpath=None, outputpath=None,
                 tmppath=None):
        self.oldpath = oldpath
        self.newpath = newpath
        self.outputpath = outputpath
        self.tmppath = tmppath

        self.verify_dirs()

    def walk(self):
        for root, dirs, files in os.walk(self.oldpath):
            relpath = path.relpath(root, self.oldpath)

            for filename in files:
                filepath = path.join(relpath, filename)
                newfilepath = path.join(self.newpath, filepath)

                if path.exists(newfilepath):
                    if path.isfile(newfilepath):
                        # modify file
                        pass

                    elif path.isdir(newfilepath):
                        # rm file
                        # add dir
                        pass

                else:
                    # rm file
                    pass

                print(filepath)

            for dirname in dirs:
                dirpath = path.join(relpath, dirname)
                newdirpath = path.join(self.newpath, dirpath)

                if path.exists(newdirpath):
                    if path.isfile(newdirpath):
                        # rm dir
                        # add file
                        pass

                    elif path.isdir(newdirpath):
                        # modify dir
                        pass

                else:
                    # rm dir
                    pass

                print(dirpath)

        for root, dirs, files in os.walk(self.newpath):
            relpath = path.relpath(root, self.newpath)

            for filename in files:
                filepath = path.join(relpath, filename)
                oldfilepath = path.join(self.oldpath, filepath)

                if path.exists(oldfilepath):
                    if path.isfile(oldfilepath):
                        # modify file
                        pass

                    elif path.isdir(oldfilepath):
                        # rm dir
                        # add file
                        pass

                else:
                    # add file
                    pass

                print(filepath)

            for dirname in dirs:
                dirpath = path.join(relpath, dirname)
                olddirpath = path.join(self.oldpath, dirpath)

                if path.exists(olddirpath):
                    if path.isfile(olddirpath):
                        # rm file
                        # add dir
                        pass

                    elif path.isdir(olddirpath):
                        # modify dir
                        pass

                else:
                    # add dir
                    pass

                print(dirpath)

    def verify_dirs(self):
        if self.oldpath is None:
            raise PrepError("oldpath must be set")
        if not (path.isdir(self.oldpath)):
            raise PrepError("oldpath must be directory")

        if self.newpath is None:
            raise PrepError("newpath must be set")
        if not (path.isdir(self.newpath)):
            raise PrepError("newpath must be directory")

        if self.outputpath is None:
            raise PrepError("outputpath must be set")
        if not (path.isdir(self.outputpath)):
            raise PrepError("outputpath must be directory")

        if self.tmppath is None:
            self.tmppath = tempfile.mkdtemp(prefix="combine_")
        if not (path.isdir(self.tmppath)):
            raise PrepError("tmppath must be directory")

