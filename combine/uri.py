# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import urllib2
import urlparse

from combine import Package, File

class URI:

    def __init__(self, uri, package=None, format=None, target=None):
        self.uri = uri
        self.parse = urlparse.urlparse(uri)
        self.package = package
        self.format = format
        self.target = target

    def __getitem__(self, key):
        return self.parse[key]

    def fetch(self, target=None):
        parse = self.parse

        # local file
        if parse.scheme == "file":
            self.handle = File(parse.path, "r", format=self.format)

        # package file
        elif parse.scheme == "package":
            if self.package is None:
                raise Exception("No package specified")

            self.handle = self.package.open(parse.path, "r", format=self.format)

        # remote http resource
        elif parse.scheme in ("http", "https"):
            self.handle = urllib2.urlopen(uri)

        else:
            raise Exception("Unsupported URI scheme %s" % (parse.scheme))

        # write directly to file if requested, and then open that
        if target:
            with File(target, "w") as fh:
                fh.write(self.handle.read())

            self.handle.close()
            self.handle = File(target, "r")

        return self.handle

    def __enter__(self):
        return self.fetch(target=self.target)

    def __exit__(self, type, value, trace):
        self.close()

    def close(self):
        self.handle.close()

