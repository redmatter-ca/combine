# Copyright (c) 2010 John Reese
# Licensed under the MIT license

import yaml

from combine import CombineError

MANIFEST_FORMAT = 1

class Manifest:

    def __init__(self):
        self.properties = {"manifest-format": MANIFEST_FORMAT}
        self.actions = []

    def add_property(self, name, value):
        self.properties[name] = value

    def add_action(self, action):
        self.actions.append(action)

    def to_dict(self):
        """
        Generate a dictionary representation of the Manifest object.
        """

        return dict(self.properties, actions=self.actions)

    @classmethod
    def from_dict(cls, data):
        """
        Given a dictionary object, generate a new Manifest object.
        """

        format = data["manifest-format"]
        if (format > MANIFEST_FORMAT or format < 0):
            raise CombineError("Unsupported manifest format")

        mft = Manifest()

        for key, value in data.items():
            if key == "actions":
                for action in value:
                    mft.add_action(dict(action))
            else:
                mft.add_property(key, value)

        return mft

    def to_yaml(self):
        """
        Generate a YAML data string representing the Manifest object.
        """

        str = yaml.safe_dump(self.to_dict(), default_flow_style=False)

        return str

    @classmethod
    def from_yaml(cls, str):
        """
        Given a string of YAML data, generate a new Manifest object.
        """

        data = yaml.safe_load(str)
        return cls.from_dict(data)
