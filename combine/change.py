# Copyright (c) 2010 John Reese
# Licensed under the MIT license

class Change:

    def __init__(self, action, filename):
        self.action = action
        self.filename = filename

    def to_dict(self):
        """
        Generate a dictionary representation of the Change object.
        """

        return {
            "action": self.action,
            "filename": self.filename,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Given a dictionary object, generate a new Change object.
        """

        change = Change(data["action"], data["filename"])

        return change
