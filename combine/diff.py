# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import os
from os import path

from fnmatch import fnmatch
import filecmp
import hashlib
from  platform import system
import tempfile

from combine import Config, Manifest, Package, File
from combine.hash import sha1
from combine.formats import extension

class Diff:

    def _walk(self, oldpath, newpath):
        oldfiles = []
        newfiles = []

        includes = eval(Config.get("actions", "include"))
        excludes = eval(Config.get("actions", "exclude"))

        for root, dirs, files in os.walk(oldpath):
            relpath = path.relpath(root, oldpath)

            if relpath == ".":
                relpath = ""

            for filename in files:
                filepath = path.join(relpath, filename)

                if (any(map(lambda glob: fnmatch(filepath, glob), excludes))):
                    continue
                if (any(map(lambda glob: fnmatch(filepath, glob), includes))):
                    oldfiles.append(filepath)

        for root, dirs, files in os.walk(newpath):
            relpath = path.relpath(root, newpath)

            if relpath == ".":
                relpath = ""

            for filename in files:
                filepath = path.join(relpath, filename)

                if (any(map(lambda glob: fnmatch(filepath, glob), excludes))):
                    continue
                if (any(map(lambda glob: fnmatch(filepath, glob), includes))):
                    newfiles.append(filepath)

        unmodified, modified, removed = filecmp.cmpfiles(oldpath, newpath,
                                                         oldfiles, shallow=False)
        unmodified, modified, added = filecmp.cmpfiles(oldpath, newpath,
                                                       newfiles, shallow=False)

        return unmodified, modified, added, removed

    def generate_update(self, currentver, currentpath, updatever, updatepath,
                        platform=None):
        """
        Given the current version/path and update version/path, generate a
        manifest, package, and individual update files in the appropriate
        locations and formats as specified by the configuration files.
        """

        manifest = Manifest()
        manifest.add_property("current-version", currentver)
        manifest.add_property("update-version", updatever)

        if platform is None:
            platform = system()

        unmodified, modified, added, removed = self._walk(currentpath, updatepath)

        fileformat = Config.get("formats", "file")
        archiveformat = Config.get("formats", "archive")

        packageextension = extension(archiveformat, dot=False)
        packagepath = Config.get("paths", "package",
                                 vars={"platform": platform,
                                       "current_version": currentver,
                                       "update_version": updatever,
                                       "extension": packageextension,
                                      })

        # build the package archive
        with Package() as package:

            for filename in unmodified:
                fullname = filename + extension(fileformat)
                fulluri = Config.get("uris", "file",
                                     vars={"platform": platform,
                                           "update_version": updatever,
                                           "filename": fullname,
                                          })

                filepath = Config.get("paths", "file",
                                     vars={"platform": platform,
                                           "update_version": updatever,
                                           "filename": fullname,
                                          })
                with File(filepath, mode="w") as fh:
                    fh.compress(path.join(updatepath, filename))

                manifest.add_action({
                    "action": "verify",
                    "filename": filename,
                    "sha1-before": sha1(path.join(updatepath, filename)),
                    "full-uri": fulluri,
                    "full-format": fileformat,
                })

            for filename in modified:
                fullname = filename + extension(fileformat)
                fulluri = Config.get("uris", "file",
                                     vars={"platform": platform,
                                           "update_version": updatever,
                                           "filename": fullname,
                                          })

                filepath = Config.get("paths", "file",
                                     vars={"platform": platform,
                                           "update_version": updatever,
                                           "filename": fullname,
                                          })
                with File(filepath, mode="w") as fh:
                    fh.compress(path.join(updatepath, filename))

                with package.open(filename, "w") as fh:
                    fh.compress(path.join(updatepath, filename))

                manifest.add_action({
                    "action": "replace",
                    "filename": filename,
                    "sha1-before": sha1(path.join(currentpath, filename)),
                    "sha1-after": sha1(path.join(updatepath, filename)),
                    "full-uri": "package:///" + filename,
                    "full-format": "raw",
                })

            for filename in added:
                with package.open(filename, "w") as fh:
                    fh.compress(path.join(updatepath, filename))

                manifest.add_action({
                    "action": "create",
                    "filename": filename,
                    "sha1-after": sha1(path.join(updatepath, filename)),
                    "full-uri": "package:///" + filename,
                    "full-format": "raw",
                })

            for filename in removed:
                manifest.add_action({
                    "action": "delete",
                    "filename": filename,
                })

            package.write(packagepath)

        manifest.add_property("package-sha1", sha1(packagepath))
        manifest.add_property("package-format", archiveformat)
        manifest.add_property("package-uri", Config.get("uris", "package",
                                 vars={"platform": platform,
                                       "current_version": currentver,
                                       "update_version": updatever,
                                       "extension": packageextension,
                                      }))

        manifestpath = Config.get("paths", "manifest",
                                  vars={"platform": platform,
                                        "current_version": currentver,
                                       })

        with File(manifestpath, mode="w") as mh:
            mh.write(manifest.to_yaml())

