# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import yaml

from combine import Change, CombineError

MANIFEST_FORMAT = 1

class Manifest:

    def __init__(self, oldver, newver):
        self.oldver = oldver
        self.newver = newver

        self.changes = []

    def add_change(self, change):
        self.changes.append(change)

    def to_dict(self):
        """
        Generate a dictionary representation of the Manifest object.
        """

        return {
            "current-version": self.oldver,
            "latest-version": self.newver,
            "manifest-format": MANIFEST_FORMAT,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Given a dictionary object, generate a new Manifest object.
        """

        format = data["manifest-format"]
        if (format > MANIFEST_FORMAT or format < 0):
            raise CombineError("Unsupported manifest format")

        mft = Manifest(data["current-version"], data["latest-version"])

        for change in data["changes"]:
            mft.add_change(Change.from_dict(change))

        return mft

    def to_yaml(self):
        """
        Generate a YAML data string representing the Manifest object.
        """

        str = yaml.safe_dump(self.to_dict(), default_flow_style=False)
        str += yaml.safe_dump({"changes": [c.to_dict() for c in self.changes]},
                             default_flow_style=False)

        return str

    @classmethod
    def from_yaml(cls, str):
        """
        Given a string of YAML data, generate a new Manifest object.
        """

        data = yaml.safe_load(str)
        return cls.from_dict(data)
