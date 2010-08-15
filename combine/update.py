# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import os
from os import path

import shutil
import tempfile

from combine import sha1, Manifest, Package, File, URI

class Update:

    def __init__(self, currentver, manifesturi):
        """
        Fetch a manifest and verify that it matches the given version.
        """

        # fetch the manifest
        with URI(manifesturi) as uri:
            manifest = Manifest.from_yaml(uri.read())

        # verify versions match
        if currentver != manifest["current-version"]:
            raise Exception("Current version does not match manifest")

        self.manifest = manifest
        self.package = None

    def apply(self, installpath):
        """
        Apply the manifest against the given installation path.
        """

        self.installpath = installpath
        manifest = self.manifest

        # fetch and verify package
        if "package-uri" in manifest:
            packageuri = URI(manifest["package-uri"])
            packagename = path.basename(packageuri["path"])
            packagepath = path.join(tempfile.gettempdir(), packagename)

            packageformat = None
            if "package-format" in manifest:
                packageformat = manifest["package-format"]

            # fetch package, or use from existing location if already fetched
            if not path.isfile(packagepath):
                packageuri.fetch(packagepath)
            packageuri.close()

            # integrity check
            if "package-sha1" in manifest:
                packagesha1 = sha1(packagepath)
                if not packagesha1 == manifest["package-sha1"]:
                    raise Exception("Package integrity check failed")

            self.package = Package(packagepath, packageformat)

        # create spot for backup files
        self.backuppath = tempfile.mkdtemp(prefix="update_")

        # start applying actions
        try:
            for info in manifest.actions:
                self._action(info)

        # handle update errors by rolling back
        except Exception as err:
            print("Exception caught; beginning rollback")

            for root, dirs, files in os.walk(self.backuppath):
                relpath = path.relpath(root, self.backuppath)

                if relpath == ".":
                    relpath = ""

                for filename in files:
                    filepath = path.join(relpath, filename)

                    print("Rolling back file %s" % (filepath))

                    self._restore(filepath)

            print("Rollback completed; raising exception")
            raise

        # clean up
        finally:
            self.cleanup = False
            shutil.rmtree(self.backuppath, onerror=self._onerror)

            self.package.close()
            os.remove(packagepath)

            if self.cleanup:
                return self.backuppath

    def _onerror(self, func, filepath, error):
        self.cleanup = True

    def _backup(self, filename, delete=True):
        ipath = path.join(self.installpath, filename)
        bpath = path.join(self.backuppath, filename)

        bdir = path.dirname(bpath)
        if not path.isdir(bdir):
            os.makedirs(bdir)

        shutil.copy(ipath, bpath)

        if delete:
            os.remove(ipath)

    def _restore(self, filename):
        ipath = path.join(self.installpath, filename)
        bpath = path.join(self.backuppath, filename)

        idir = path.dirname(ipath)
        if not path.isdir(idir):
            os.makedirs(idir)

        if path.isfile(ipath):
            os.remove(ipath)

        shutil.copy(bpath, ipath)
        os.remove(bpath)

    def _action(self, info):
        action = info["action"]
        filename = info["filename"]
        fullpath = path.join(self.installpath, filename)

        # verify file integrity and attempt to repair if corrupted
        if action == "verify":
            hash = info["sha1-before"]
            if not sha1(fullpath) == hash:
                if "full-uri" in info:
                    fullformat = None
                    if "full-format" in info:
                        fullformat = info["full-format"]

                    self._backup(filename)
                    with URI(info["full-uri"], package=self.package, format=fullformat,
                             target=fullpath):
                        if not sha1(fullpath) == hash:
                            raise Exception("Integrity check and repair failed")

                else:
                    raise Exception("Integrity check failed with no repair")

        # create a new file and verify integrity
        elif action == "create":
            hash = info["sha1-after"]
            if "full-uri" in info:
                fullformat = None
                if "full-format" in info:
                    fullformat = info["full-format"]

                with URI(info["full-uri"], package=self.package, format=fullformat,
                         target=fullpath):
                    if not sha1(fullpath) == hash:
                        raise Exception("Created file failed integrity check")

            else:
                raise Exception("Create action has no URI")

        # replace file and verify replacement integrity
        elif action == "replace":
            hash = info["sha1-after"]
            if "full-uri" in info:
                fullformat = None
                if "full-format" in info:
                    fullformat = info["full-format"]

                self._backup(filename)
                with URI(info["full-uri"], package=self.package, format=fullformat,
                         target=fullpath):
                    if not sha1(fullpath) == hash:
                        raise Exception("Replacement file failed integrity check")

            else:
                raise Exception("Replacement action has no URI")

        # delete a file with little recourse
        elif action == "delete":
            self._backup(filename, delete=True)

        # intentional exception to test rollbacks
        elif action == "exception":
            raise Exception("Intentional exception raised")

        # /shrug
        else:
            raise Exception("Unsupported action %s" % (action))

