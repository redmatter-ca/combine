# Copyright (c) 2010 John Reese
# Licensed under the MIT license

from os import path
import hashlib

def sha1(filepath):
    """
    Generate a SHA1 hash for a file.
    """

    filepath = path.normpath(filepath)

    if not path.isfile(filepath):
        return ""

    with open(filepath, "rb") as fh:
        data = fh.read()

        hash = hashlib.sha1()
        hash.update(data)

        return hash.hexdigest()

