# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import os
from os import path
import sys
import time
import traceback
import urllib
import urllib2
import urlparse

from combine import Package, File, log

class URI:

    def __init__(self, uri, package=None, format=None, target=None):
        self.uri = uri
        self.parse = urlparse.urlparse(uri)
        self.package = package
        self.format = format
        self.target = target
        self.handle = None

    def __getitem__(self, key):
        return self.parse.__getattribute__(key)

    def fetch(self, target=None):
        parse = self.parse

        # local file
        if parse.scheme == "file":
            self.handle = File(parse.path, "r", format=self.format)

            if target:
                self.handle.decompress(target)
                self.handle.close()
                self.handle = File(target, "r")

        # package file
        elif parse.scheme == "package":
            if self.package is None:
                raise Exception("No package specified")

            filename = parse.path.lstrip("/")
            self.handle = self.package.open(filename, "r", format=self.format)

            if target:
                self.handle.decompress(target)
                self.handle.close()
                self.handle = File(target, "r")

        # remote http resource
        elif parse.scheme in ("http", "https"):
            failure = True
            tries = 0

            while failure:
                failure = False

                try:
                    if target:
                        target = path.normpath(target)
                        log.info("Downloading {0} to file {1}".format(self.uri, target))
                        downloadpath, headers = urllib.urlretrieve(self.uri)
                        self.handle = File(downloadpath, "r", format=self.format)
                        self.handle.decompress(target)
                        self.handle.close()
                        self.handle = File(target, "r")
                    else:
                        self.handle = urllib2.urlopen(self.uri)

                except:
                    failure = True
                    if tries < 3:
                        log.info("Problem retrieving URI, retry in 3 seconds...")
                        log.debug(traceback.format_exception(sys.exc_type,
                                                             sys.exc_value,
                                                             sys.exc_traceback))
                        time.sleep(3)

                    else:
                        log.info("Failed retrieving URI")
                        raise

                finally:
                    tries += 1

            return self.handle

        else:
            raise Exception("Unsupported URI scheme {0}".format(parse.scheme))

        return self.handle

    def __enter__(self):
        return self.fetch(target=self.target)

    def __exit__(self, type, value, trace):
        self.close()

    def close(self):
        if self.handle:
            self.handle.close()

