# Copyright (c) 2010 John Reese
# Licensed under the MIT license

class Change:

    def __init__(self, action, filename):
        self.action = action
        self.filename = filename

    def to_dict(self):
        return {
            "action": self.action,
            "filename": self.filename,
        }
