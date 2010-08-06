# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import os
from os import path
import shutil
import tempfile

from combine import formats

class Package:

    def __init__(self, archive=None, format=None):
        """
        Create a new package representation, with a temporary directory for
        creating or extracting package contents.
        """

        self._open = True
        self._tempdir = tempfile.mkdtemp(prefix="combine_")

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
        Open a file descriptor in the package's workspace.
        """

        return open(path.join(self._tempdir, filename), mode)

    def read(self, filename, format=None):
        """
        Extract an existing package file into the temporary workspace.
        """

        with formats.Archive(filename, mode="r") as archive:
            archive.extractall(self._tempdir)

    def write(self, filename, format=None):
        """
        Create a new package file from the temporary workspace.
        """

        with formats.Archive(filename, mode="w") as archive:
            for root, dirs, files in os.walk(self._tempdir):
                for file in files:
                    fullpath = path.join(root, file)
                    relpath = path.relpath(fullpath, self._tempdir)
                    archive.add(fullpath, relpath)

    def close(self):
        """
        Close out any remaining file descriptors, and cleanup any temporary
        directories used by this instance.
        """

        if self._open:
            shutil.rmtree(path=self._tempdir, ignore_errors=True)

