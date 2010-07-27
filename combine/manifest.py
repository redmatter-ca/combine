# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import yaml

from combine import Change

MANIFEST_FORMAT = 1

class Manifest:

    def __init__(self, oldver, newver):
        self.oldver = oldver
        self.newver = newver

        self.changes = []

    def add_change(self, change):
        self.changes.append(change)

    def to_dict(self):
        return {
            "current-version": self.oldver,
            "latest-version": self.newver,
            "manifest-format": MANIFEST_FORMAT,
        }

    def to_yaml(self):
        str = yaml.safe_dump(self.to_dict(), default_flow_style=False)
        str += yaml.safe_dump({"changes": [c.to_dict() for c in self.changes]},
                             default_flow_style=False)

        return str

