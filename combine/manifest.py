# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import yaml

from combine import Change

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
            "changes": [c.to_dict() for c in self.changes],
        }

    def to_yaml(self):
        print yaml.safe_dump(self.to_dict(), default_flow_style=False)

