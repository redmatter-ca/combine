# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import os
from os import path
import shutil
import tempfile

from combine import Archive, File

class Package:

    def __init__(self, archive=None, format=None):
        """
        Create a new package representation, with a temporary directory for
        creating or extracting package contents.
        """

        self._open = True
        self._tempdir = tempfile.mkdtemp(prefix="combine_")
        self._fhs = {}

        if archive:
            self.read(archive, format)

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, trace):
        self.close()

    def open(self, filename, mode="r"):
        """
        Open a file descriptor in the package's workspace. If the file
        handle is still open from a previous operation, raise an error.
        """

        # make sure the file handle is not already open
        if filename in self._fhs:
            fh = self._fhs[filename]
            if fh.closed:
                del self._fhs[filename]
            else:
                raise Exception("File %s already open" % (filename))

        # create directory structure if needed
        if mode == "w":
            dir = path.dirname(filename)
            if not path.isdir(dir):
                os.makedirs(dir)

        # retrieve and track the file handle
        fh = File(path.join(self._tempdir, filename), mode)
        self._fhs[filename] = fh

        return fh

    def read(self, filename, format=None):
        """
        Extract an existing package file into the temporary workspace.
        """

        with Archive(filename, mode="r") as archive:
            archive.extractall(self._tempdir)

    def write(self, filename, format=None):
        """
        Create a new package file from the temporary workspace.
        """

        for fn, fh in self._fhs.items():
            if not fh.closed:
                raise Exception("File %s still open" % (fn))

        with Archive(filename, mode="w") as archive:
            for root, dirs, files in os.walk(self._tempdir):
                for file in files:
                    fullpath = path.join(root, file)
                    relpath = path.relpath(fullpath, self._tempdir)
                    archive.add(fullpath, relpath)

    def close(self):
        """
        Close out any remaining file handles, and cleanup any temporary
        directories used by this instance.
        """

        for fn, fh in self._fhs.items():
            if not fh.closed:
                fh.close()

        if self._open:
            shutil.rmtree(path=self._tempdir, ignore_errors=True)

