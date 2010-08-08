# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import urllib2
import urlparse

from combine import Package, File

class URI:

    def __init__(self, uri, package=None, format=None):
        self.uri = uri

        parse = urlparse.urlparse(uri)

        # local file
        if parse.scheme == "file":
            self.handle = File(parse.path, "r", format=None)

        # package file
        elif parse.scheme == "package":
            if package is None:
                raise Exception("No package specified")

            self.handle = package.open(parse.path, "r", format=None)

        # remote http resource
        elif parse.scheme in ("http", "https"):
            self.handle = urllib2.urlopen(uri)

        else:
            raise Exception("Unsupported URI scheme %s" % (parse.scheme))

    def __enter__(self):
        return self.handle

    def __exit__(self, type, value, trace):
        self.close()

    def read(self):
        return self.handle.read()

    def close(self):
        self.handle.close()

