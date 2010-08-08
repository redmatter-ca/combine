# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import hashlib

def sha1(filepath):
    """
    Generate a SHA1 hash for a file.
    """

    fh = open(filepath, "rb")
    data = fh.read()

    hash = hashlib.sha1()
    hash.update(data)

    return hash.hexdigest()

