# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import os
from os import path
import zipfile
import tarfile

def detect(filename):
    """
    Auto-detect file format based on file extension.
    """

    root, ext = path.splitext(filename)
    root, ext2 = path.splitext(root)

    if ext == ".zip":
        format = "zip"

    elif ext == ".tbz2" or (ext == ".bz2" and ext2 == ".tar"):
        format = "tar-bzip2"
    elif ext == ".bz2":
        format = "bzip2"

    elif ext == ".tgz" or (ext == ".gz" and ext2 == ".tar"):
        format = "tar-gzip"
    elif ext == ".gz":
        format = "gzip"

    else:
        format = "raw"

    return format

def extension(format, dot=True):
    """
    Return the canonical file extension for a given format.
    """

    if format == "zip":
        extension = "zip"

    elif format == "tar-bzip2":
        extension = "tbz2"
    elif format == "bzip2":
        extension = "bz2"

    elif format == "tar-gzip":
        extension = "tgz"
    elif format == "gzip":
        extension = "gz"

    else:
        extension = ""

    if dot:
        return "." + extension
    else:
        return extension

class Archive:
    """
    Generic archive manipulation class, acting as a wrapper for zipfile and
    tarfile modules.
    """

    def __init__(self, filename, mode="r", format=None):
        """
        Load an appropriate archive file descriptor for the given filename and
        read/write access mode.
        """

        if not (mode == "r" or mode == "w"):
            raise Exception("Unsupported mode")

        # verify mode versus file existence
        if mode == "r" and not path.isfile(filename):
            raise Exception("Archive file does not exist")

        # create directory structure if needed
        if mode == "w":
            dir = path.dirname(filename)
            if not path.isdir(path.dirname(filename)):
                os.makedirs(dir)

        # auto-detect format
        if format is None:
            format = detect(filename)

        # open the file descriptors
        if format == "zip":
            self.archive = zipfile.ZipFile(filename, mode)

        elif format == "tar-bzip2":
            tmode = mode + ":bz2"
            self.archive = tarfile.open(filename, tmode)

        elif format == "tar-gzip":
            tmode = mode + ":gz"
            self.archive = tarfile.open(filename, tmode)

        else:
            raise Exception("Unsupport archive format: %s" % format)

        # instance state
        self.filename = filename
        self.format = format
        self.mode = mode
        self.closed = False

    def __enter__(self):
        return self
    def __exit__(self, type, value, trace):
        self.close()
    
    def extractall(self, directory):
        """
        Extract all files from an archive to an existing directory
        """

        if not self.mode == "r":
            raise Exception("Archive not opened for read access")

        if not path.isdir(directory):
            raise Exception("Directory does not exist")

        if self.format == "zip":
            self.archive.extractall(directory)

        elif self.format == "tar-bzip2" or self.format == "tar-gzip":
            self.archive.extractall(directory)

    def add(self, filename, arcname):
        """
        Add a file to a new archive.
        """

        if not self.mode == "w":
            raise Exception("Archive not opened for read access")

        if not path.isfile(filename):
            raise Exception("File does not exist")

        if self.format == "zip":
            self.archive.write(filename, arcname)

        elif self.format == "tar-bzip2" or self.format == "tar-gzip":
            self.archive.add(filename, arcname)

    def close(self):
        """
        Close out any file descriptors.
        """

        if self.format == "zip":
            self.archive.close()

        elif self.format == "tar-bzip2" or self.format == "tar-gzip":
            self.archive.close()
